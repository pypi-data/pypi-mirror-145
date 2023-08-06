from tensorflow.keras.layers import LSTM, Dropout, Dense, Layer, Concatenate, LayerNormalization, Conv1D, GlobalAveragePooling1D
from tensorflow.keras import Input, Model
from tensorflow.keras.models import Sequential
import time
import xgboost as xgb
from sklearn.model_selection import train_test_split
from tcn import TCN

#   ------------------------  lstm  -------------------------- 
def lstm_model_custmize(look_back, look_forward, n_features, dropout=0.5, print_summary=False, n_neurons = [128]):
  modelLSTM = Sequential(name='LSTM_Model_customized')
  modelLSTM.add(LSTM(n_neurons[0], input_shape=(look_back, n_features), name='LSTM_layer_1', return_sequences=True))
  # modelLSTM.add(Dropout(dropout, name='dropout_layer_1'))
  if len(n_neurons) == 1:
    modelLSTM.add(LSTM(look_forward, name='LSTM_layer_2'))
  for layer_i in range(1, len(n_neurons) - 1):
    modelLSTM.add(LSTM(n_neurons[layer_i], input_shape=(n_neurons[layer_i - 1], n_features), name='LSTM_layer_'+str(layer_i + 1), return_sequences=True))
    # modelLSTM.add(Dropout(dropout, name='dropout_layer_'+str(layer_i + 1)))
  if len(n_neurons) > 1:
    modelLSTM.add(LSTM(n_neurons[-1], input_shape=(n_neurons[-2], 1), name='LSTM_layer_'+str(len(n_neurons))+''))
  modelLSTM.add(Dense(look_forward, name='dense_output_layer'))
  modelLSTM.compile(loss='mean_squared_error', optimizer='adam')
  if print_summary:
    print(modelLSTM.summary())
  return modelLSTM


#  --------------------------- TCN ------------------------------
def tcn_model(look_back, n_features, look_forward, batch_size=None, print_summary=True, n_neurons=[128], dropout=0.5):
  tcn_units = []
  for index in range(len(n_neurons)):
    tcn_units.append('x'+str(index)+'_')
  
  input_ = Input(batch_shape=(batch_size, look_back, n_features), name='Input_Layer')
  if len(n_neurons) == 1:
    tcn_units[0] = TCN(nb_filters=n_neurons[0], kernel_size=2, nb_stacks=2, dilations=[1, 2, 4, 8, 16, 32], 
                   padding='causal', use_skip_connections=True, dropout_rate=dropout, return_sequences=False, 
                   activation='relu', kernel_initializer='he_normal', name = 'TCN_Layer_1', use_batch_norm=True)(input_)
  else:
    tcn_units[0] = TCN(nb_filters=n_neurons[0], kernel_size=2, nb_stacks=2, dilations=[1, 2, 4, 8, 16, 32], 
                   padding='causal', use_skip_connections=True, dropout_rate=dropout, return_sequences=True, 
                   activation='relu', kernel_initializer='he_normal', name = 'TCN_Layer_1', use_batch_norm=True)(input_)
  for index in range(len(tcn_units) - 2):
    tcn_units[index + 1] = TCN(nb_filters=n_neurons[index + 1], kernel_size=2, nb_stacks=2, dilations=[1, 2, 4, 8, 16, 32], 
                  padding='causal', use_skip_connections=True, dropout_rate=dropout, return_sequences=True, 
                  activation='relu', kernel_initializer='he_normal',
                  name = 'TCN_Layer_' + str(index + 2), use_batch_norm=True)(tcn_units[index])  # The TCN layer .
  if len(n_neurons) > 1:
    tcn_units[-1] = TCN(nb_filters=n_neurons[-1], kernel_size=2, nb_stacks=2, dilations=[1, 2, 4, 8, 16, 32], 
                  padding='causal', use_skip_connections=True, dropout_rate=dropout, return_sequences=False, 
                  activation='relu', kernel_initializer='he_normal',
                  name = 'TCN_Layer_' + str(len(n_neurons) + 1), use_batch_norm=True)(tcn_units[-2])  # The TCN layer .
  output_ = Dense(look_forward, name='Dense_Layer')(tcn_units[-1])
  modelTCN = Model(inputs=[input_], outputs=[output_], name='TCN_Model_customized')
  modelTCN.compile(optimizer='adam', loss='mse')
  if print_summary:
    print(modelTCN.summary())
  return modelTCN


# ----------------- Transformer  ---------------------------- 
class Time2Vector(Layer):
    def __init__(self, seq_len, **kwargs):
        super(Time2Vector, self).__init__()
        self.seq_len = seq_len

    def build(self, input_shape):
        '''Initialize weights and biases with shape (batch, seq_len)'''
        self.weights_linear = self.add_weight(name='weight_linear',
                                shape=(int(self.seq_len),),
                                initializer='uniform',
                                trainable=True)
        self.bias_linear = self.add_weight(name='bias_linear',
                                shape=(int(self.seq_len),),
                                initializer='uniform',
                                trainable=True)

        self.weights_periodic = self.add_weight(name='weight_periodic',
                                shape=(int(self.seq_len),),
                                initializer='uniform',
                                trainable=True)
        self.bias_periodic = self.add_weight(name='bias_periodic',
                                shape=(int(self.seq_len),),
                                initializer='uniform',
                                trainable=True)
    
    def call(self, x):
        '''Calculate linear and periodic time features'''
        x = tf.math.reduce_mean(x[:,:,1:], axis=-1) 
        time_linear = self.weights_linear * x + self.bias_linear # Linear time feature
        time_linear = tf.expand_dims(time_linear, axis=-1) # Add dimension (batch, seq_len, 1)
        time_periodic = tf.math.sin(tf.multiply(x, self.weights_periodic) + self.bias_periodic)
        time_periodic = tf.expand_dims(time_periodic, axis=-1) # Add dimension (batch, seq_len, 1)
        return tf.concat([time_linear, time_periodic], axis=-1) # shape = (batch, seq_len, 2)
        
    def get_config(self): # Needed for saving and loading model with custom layer
        config = super().get_config().copy()
        config.update({'seq_len': self.seq_len})
        return config

class TransformerEncoder(Layer):
    def __init__(self, d_k, d_v, n_heads, ff_dim, dropout=0.1, **kwargs):
        super(TransformerEncoder, self).__init__()
        self.d_k = d_k
        self.d_v = d_v
        self.n_heads = n_heads
        self.ff_dim = ff_dim
        self.attn_heads = list()
        self.dropout_rate = dropout

    def build(self, input_shape):
        self.attn_multi = MultiAttention(self.d_k, self.d_v, self.n_heads)
        self.attn_dropout = Dropout(self.dropout_rate)
        self.attn_normalize = LayerNormalization(input_shape=input_shape, epsilon=1e-6)

        self.ff_conv1D_1 = Conv1D(filters=self.ff_dim, kernel_size=1, activation='relu')
        # input_shape[0]=(batch, seq_len, 7), input_shape[0][-1] = 7 
        self.ff_conv1D_2 = Conv1D(filters=input_shape[0][-1], kernel_size=1) 
        self.ff_dropout = Dropout(self.dropout_rate)
        self.ff_normalize = LayerNormalization(input_shape=input_shape, epsilon=1e-6)    

    def call(self, inputs): # inputs = (in_seq, in_seq, in_seq)
        attn_layer = self.attn_multi(inputs)
        attn_layer = self.attn_dropout(attn_layer)
        attn_layer = self.attn_normalize(inputs[0] + attn_layer)

        ff_layer = self.ff_conv1D_1(attn_layer)
        ff_layer = self.ff_conv1D_2(ff_layer)
        ff_layer = self.ff_dropout(ff_layer)
        ff_layer = self.ff_normalize(inputs[0] + ff_layer)
        return ff_layer 
    
    def get_config(self): # Needed for saving and loading model with custom layer
        config = super().get_config().copy()
        config.update({'d_k': self.d_k,
                   'd_v': self.d_v,
                   'n_heads': self.n_heads,
                   'ff_dim': self.ff_dim,
                   'attn_heads': self.attn_heads,
                   'dropout_rate': self.dropout_rate})
        return config

    
def transformer_model_custmize(look_back, look_forward, n_features, n_heads = 5, d_k = 256, d_v = 256, ff_dim = 256, dropout = 0.5, num_hidden = 64, print_summary=True):
    '''Initialize time and transformer layers'''
    time_embedding = Time2Vector(look_back)
    attn_layer1 = TransformerEncoder(d_k, d_v, n_heads, ff_dim)
    attn_layer2 = TransformerEncoder(d_k, d_v, n_heads, ff_dim)
    attn_layer3 = TransformerEncoder(d_k, d_v, n_heads, ff_dim)
    '''Construct model'''
    in_seq = Input(shape=(look_back, n_features))
    x = time_embedding(in_seq)
    x = Concatenate(axis=-1)([in_seq, x])
    x = attn_layer1((x, x, x))
    x = attn_layer2((x, x, x))
    x = attn_layer3((x, x, x))
    x = GlobalAveragePooling1D(data_format='channels_first')(x)
    x = Dropout(dropout)(x)
    # active_func = trial.suggest_categorical('active_function', ['relu', 'entropy'])
    x = Dense(num_hidden, activation='relu')(x)
    x = Dropout(dropout)(x)
    out = Dense(look_forward, activation='linear')(x)
    model = Model(inputs=in_seq, outputs=out)
    model.compile(loss='mse', optimizer='adam', metrics=['mse']) #, 'mape'])
    if print_summary:
      print(model.summary())
    return model

#------------------  Xgb Classification ----------------------------------------------------
def train_xgb(df, label_column, num_class, epoch = 100):
    start_time = time.time()
    y_data = df[label_column]
    x_data = df.drop(columns = [label_column])
    X_train, X_val, y_train, y_val = train_test_split(x_data, y_data, test_size=0.2)
    dtrain = xgb.DMatrix(X_train, label = y_train)
    dtest = xgb.DMatrix(X_val)
    params = {
    'booster': 'gbtree',
    'objective': 'multi:softmax', #多分类'multi:softmax'返回预测的类别(不是概率)，'multi:softprob'返回概率
    'num_class': num_class,
    'eval_metric': 'merror', #二分类用’auc‘，多分类用'mlogloss'或'merror'
    'max_depth': 7,
    'lambda': 15,
    'subsample': 0.75,
    'colsample_bytree': 0.75,
    'min_child_weight': 1,
    'eta': 0.025,  # lr
    'seed': 0,
    'nthread': 8,
    'silent': 1,
    'gamma': 0.15,
    'learning_rate': 0.01}
    watchlist = [(dtrain, 'train')]
    model = xgb.train(params, dtrain, num_boost_round = epoch, evals = watchlist)
    y_pred = model.predict(dtest)
    end_time = time.time()
    print('time cost : ', round((end_time - start_time) / 60, 2), 'min')
    return model, y_pred, y_val