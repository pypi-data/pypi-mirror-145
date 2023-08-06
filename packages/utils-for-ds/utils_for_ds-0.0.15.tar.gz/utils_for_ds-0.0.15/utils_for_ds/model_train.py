from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dropout, Dense, Concatenate, GlobalAveragePooling1D
from tensorflow.keras import Input, Model
from tcn import TCN
from keras.callbacks import EarlyStopping
import tensorflow as tf
import numpy as np
import time
import optuna
from optuna.integration import TFKerasPruningCallback
from optuna.trial import TrialState
from utils_for_ds import data_utils
from utils_for_ds import model_customize

# ------------  Optuna ----------------
def time_model_with_data_split(df, label_column, train_start, train_end,  look_back, look_forward, column_set_index = 0, split_n = 30, n_neurons = [128],
                          transformer_args = [5, 256, 256, 256], print_model_summary = True, dropout = 0.5, epochs = 30, patience = 5, early_stop = True,
                          save_model = False, model_path = 'model.hdf5', save_weight = False, checkpoint_path = '', model_name = 'lstm', enable_optuna = False, epochs_each_try = 10,
                          n_trials = 10, show_loss = True):
  start_time = time.time()
  tf.random.set_seed(1)
  df = data_utils.switch_y_column(df, column_name=label_column)
  if column_set_index:
    df.set_index(column_set_index, inplace=True)
  train_data = df[train_start : train_end]
  X_train_seq, y_train_seq = data_utils.split_sequence(train_data.values, look_back = look_back, look_forward = look_forward)
  X_train_seq, y_train_seq, X_val_seq, y_val_seq = data_utils.time_split_dataset(X_train_seq, y_train_seq, split_n = split_n)
  n_features = X_train_seq.shape[2]

  def create_lstm_model(trial):
        n_layers = trial.suggest_int("n_layers", 1, 5)
        model = Sequential()
        n_units = np.zeros(n_layers, dtype=np.int64)
        n_units[0] = trial.suggest_int("units_L1", 32, 256)
        dropout = trial.suggest_uniform(f"dropout", 0.01, 0.5)
        if n_layers == 1:
          model.add(LSTM(n_units[0], input_shape=(look_back, n_features), return_sequences=False))
        else:
          model.add(LSTM(n_units[0], input_shape=(look_back, n_features), return_sequences=True))
        for i in range(1, n_layers - 1):
          n_units[i] = trial.suggest_int("units_L"+str(i+1), 32, 256)
          model.add(LSTM(n_units[i], input_shape=(n_units[i - 1], n_features), return_sequences=True))
          model.add(Dropout(dropout))
        if n_layers > 1:
          n_units[-1] = trial.suggest_int("units_L"+str(n_layers), 32, 256)
          model.add(LSTM(n_units[-1], input_shape=(n_units[-2], n_features), return_sequences=False))
        model.add(Dropout(dropout))
        model.add(Dense(look_forward))
        model.compile(loss='mean_squared_error', optimizer='adam', metrics=['mse'])
        return model
  
  def create_tcn_model(trial):
    tcn_batch_size = None # 512 # 1024
    n_layers = trial.suggest_int("n_layers", 1, 5)
    n_units = np.zeros(n_layers, dtype=np.int64)
    layer_names = []
    for index in range(n_layers):
        layer_names.append('x'+str(index)+'_')
    input_ = Input(batch_shape=(tcn_batch_size, look_back, n_features), name='Input_Layer')
    n_units[0] = trial.suggest_int("units_L1", 32, 256)
    dropout = trial.suggest_uniform(f"dropout", 0.01, 0.5)
    if n_layers == 1:
        layer_names[0] = TCN(nb_filters=n_units[0], kernel_size=2, nb_stacks=2, dilations=[1, 2, 4, 8, 16, 32], 
                           padding='causal', use_skip_connections=True, dropout_rate=dropout, return_sequences=False, 
                           activation='relu', kernel_initializer='he_normal', name = 'TCN_Layer_1', use_batch_norm=True)(input_)
    else:
        layer_names[0] = TCN(nb_filters=n_units[0], kernel_size=2, nb_stacks=2, dilations=[1, 2, 4, 8, 16, 32], 
                           padding='causal', use_skip_connections=True, dropout_rate=dropout, return_sequences=True, 
                           activation='relu', kernel_initializer='he_normal', name = 'TCN_Layer_1', use_batch_norm=True)(input_)
    for index in range(1, n_layers - 1):
        n_units[index] = trial.suggest_int("units_L"+str(index + 1), 32, 256)
        layer_names[index] = TCN(nb_filters=n_units[index], kernel_size=2, nb_stacks=2, dilations=[1, 2, 4, 8, 16, 32], 
                  padding='causal', use_skip_connections=True, dropout_rate=dropout, return_sequences=True, 
                  activation='relu', kernel_initializer='he_normal', name = 'TCN_Layer_' + str(index + 1), use_batch_norm=True)(layer_names[index - 1])  # The TCN layer .
    if n_layers > 1:
        n_units[-1] = trial.suggest_int("units_L"+str(n_layers), 32, 256)
        layer_names[-1] = TCN(nb_filters=n_units[-1], kernel_size=2, nb_stacks=2, dilations=[1, 2, 4, 8, 16, 32], 
                  padding='causal', use_skip_connections=True, dropout_rate=dropout, return_sequences=False, 
                  activation='relu', kernel_initializer='he_normal',
                  name = 'TCN_Layer_' + str(n_layers), use_batch_norm=True)(layer_names[-2])  # The TCN layer .
    output_ = Dense(look_forward, name='Dense_Layer')(layer_names[-1])
    model = Model(inputs=[input_], outputs=[output_], name='TCN_Model_trail')
    model.compile(loss='mean_squared_error', optimizer='adam', metrics=['mse'])
    return model
  
  def create_transformer_model(trial):
    time_embedding = Time2Vector(look_back)
    n_heads = trial.suggest_int("n_heads", 1, 16)
    d_k =    trial.suggest_int("d_k", 8, 215)
    d_v =    trial.suggest_int("d_v", 8, 512)
    ff_dim = trial.suggest_int("ff_dim", 8, 512)
    attn_layer1 = TransformerEncoder(d_k, d_v, n_heads, ff_dim)
    attn_layer2 = TransformerEncoder(d_k, d_v, n_heads, ff_dim)
    attn_layer3 = TransformerEncoder(d_k, d_v, n_heads, ff_dim)
    in_seq = Input(shape=(look_back, n_features))
    x = time_embedding(in_seq)
    x = Concatenate(axis=-1)([in_seq, x])
    x = attn_layer1((x, x, x))
    x = attn_layer2((x, x, x))
    x = attn_layer3((x, x, x))
    x = GlobalAveragePooling1D(data_format='channels_first')(x)
    dropout = trial.suggest_uniform(f"dropout", 0.01, 0.5)
    x = Dropout(dropout)(x)
    num_hidden = int(trial.suggest_loguniform("hidden", 4, 512))
    # active_func = trial.suggest_categorical('active_function', ['relu', 'entropy'])
    x = Dense(num_hidden, activation='relu')(x)
    x = Dropout(dropout)(x)
    out = Dense(look_forward, activation='linear')(x)
    model = Model(inputs=in_seq, outputs=out)
    model.compile(loss='mse', optimizer='adam', metrics=['mse']) #, 'mape'])
    return model
  
  def objective(trial):
    keras.backend.clear_session()   # Clear clutter from previous session graphs.
    if model_name == 'lstm':
      model = create_lstm_model(trial)     # Generate our trial model.
    elif model_name == 'tcn':
      model = create_tcn_model(trial)
    elif model_name == 'transformer':
      model = create_transformer_model(trial)
    else:
      model = create_lstm_model(trial)
    history = model.ﬁt(X_train_seq, y_train_seq, epochs=epochs_each_try, batch_size=512,  # None
             validation_data=(X_val_seq, y_val_seq),
             callbacks=[TFKerasPruningCallback(trial, "val_loss")],
             verbose=1)
    # score = model.evaluate(X_val_seq, y_val_seq, verbose=0)   # Evaluate the model accuracy on the validation set.
    score = history.history["val_mse"][0]  # Evaluate the model loss.
    return score
  
  if enable_optuna:
      study = optuna.create_study(direction="minimize", sampler=optuna.samplers.TPESampler(), pruner=optuna.pruners.HyperbandPruner())
      study.optimize(objective, n_trials=n_trials)   
      pruned_trials = study.get_trials(deepcopy=False, states=[TrialState.PRUNED])
      complete_trials = study.get_trials(deepcopy=False, states=[TrialState.COMPLETE])
      print("Study statistics: ")
      print("  Number of finished trials: ", len(study.trials))
      print("  Number of pruned trials: ", len(pruned_trials))
      print("  Number of complete trials: ", len(complete_trials))
      if len(complete_trials) == 0: 
        print('No trails are completed yet, please increate the n_trials or epochs_each_try and run again.')
        return None
      else:
        print("Best trial: Value :", study.best_trial.value)
        print("  Params: ")
        for key, value in study.best_trial.params.items():
          print("    {}: {}".format(key, value))

      if model_name in ['lstm', 'tcn']:
        n_neurons = np.zeros(study.best_trial.params['n_layers'], dtype=np.int64)
        for i in range(len(n_neurons)):
          column_name = 'units_L'+str(i+1)
          n_neurons[i] = study.best_trial.params[column_name]
          dropout = study.best_trial.params['dropout']
          # plot_optimization_history(study) # plot_intermediate_values(study) # plot_contour(study) # plot_param_importances(study)
      if model_name in ['transformer']:
        dropout = study.best_trial.params['dropout']
        transformer_args = [study.best_trial.params['n_heads'], study.best_trial.params['d_k'], study.best_trial.params['d_v'], study.best_trial.params['ff_dim'], study.best_trial.params['hidden']]

  if model_name == 'lstm':
    l_Model = model_customize.lstm_model_custmize(look_back=look_back, look_forward=look_forward, n_features=n_features, dropout=dropout, print_summary=print_model_summary, n_neurons = n_neurons)
  elif model_name == 'tcn':
    l_Model = model_customize.tcn_model(look_back=look_back, look_forward=look_forward, n_features=n_features, dropout=dropout, print_summary=print_model_summary, n_neurons = n_neurons)
  elif model_name == 'transformer':
    l_Model = model_customize.transformer_model_custmize(look_back, look_forward, n_features=n_features, n_heads=transformer_args[0], d_k =transformer_args[1], d_v=transformer_args[2], ff_dim=transformer_args[3], dropout=dropout, num_hidden=64, print_summary=True)
  else:
    l_Model = model_customize.lstm_model_custmize(look_back=look_back, look_forward=look_forward, n_features=n_features, dropout=dropout, print_summary=print_model_summary, n_neurons = n_neurons)
  
  if early_stop == False:
    patience = epochs

  if save_model:
    model_train = train_model(l_Model, X_train_seq, y_train_seq, X_val_seq, y_val_seq, epochs=epochs, early_stop = early_stop, patience=patience, save_model = save_model, model_path=model_path, save_weight = save_weight, checkpoint_path=checkpoint_path, show_loss = show_loss)
  else:
    model_train = train_model(l_Model, X_train_seq, y_train_seq, X_val_seq, y_val_seq, epochs=epochs, early_stop = early_stop, patience=patience, save_model = save_model, show_loss = show_loss)
  end_time = time.time()
  print('time cost : ', round((end_time - start_time) / 60, 2), 'min')
  return l_Model

# -----------    Train  ----------------   
def train_model(model, X_train_seq, y_train_seq, X_val_seq, y_val_seq,  epochs=100, early_stop = True, patience=10, 
                save_model = False, model_path='', save_weight = False, checkpoint_path='', show_loss = True):
  if not early_stop:
    patience = epochs
  early_stopping = EarlyStopping(monitor='val_loss', 
                              min_delta=0, 
                              patience=patience, 
                              verbose=0, 
                              mode='auto', 
                              baseline=None, 
                              restore_best_weights=False)
  if save_model:
    cp_callback = tf.keras.callbacks.ModelCheckpoint(model_path, 
                                                 monitor='val_loss', 
                                                 save_best_only=True, 
                                                 # save_weights_only=True,
                                                 verbose=1)
    history = model.fit(X_train_seq, y_train_seq,
                    epochs=epochs,
                    validation_data=(X_val_seq, y_val_seq),
                    shuffle=True,
                    batch_size=32,
                    verbose=1,
                    callbacks=[early_stopping, cp_callback])
    if save_weight:
      model.save_weights(checkpoint_path)
    save_model_to_path = tf.keras.callbacks.ModelCheckpoint(model_path, monitor='val_loss', save_best_only=True, verbose=1)
  else:
    history = model.fit(X_train_seq, y_train_seq,
                    epochs=epochs,
                    validation_data=(X_val_seq, y_val_seq),
                    shuffle=True,
                    batch_size=32,
                    verbose=1,
                    callbacks=[early_stopping])
  if show_loss:
    label_list = [i for i in range(0, len(history.history['loss']))]
    data_utils.show_draft_plot(datas = [history.history['loss'], history.history['val_loss']], x_label = label_list, title = 'Loss of Model', legend=['loss', 'val loss'])
  return model

# ------------- Predict ----------------
def predict_result(predict_data_list = [] , model_path=[], model_type=['lstm'], divideby = [1]):
  predict_list = []
  for index in range(len(model_path)):
    if model_type[index] in ['lstm', 'tcn', 'transformer']:
      model_file = model_path[index]
      prediction = model_file.predict(predict_data_list[index])
      pred = np.array(prediction[-1]) * divideby[index]
      predict_list.append(pred)
    if model_type[index] in ['linear', 'xgb']:
      model_file = model_path[index]
      prediction = model_file.predict(predict_data_list[index])
      pred = np.array(prediction) * divideby[index]
      predict_list.append(prediction)
  return predict_list