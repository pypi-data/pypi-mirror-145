import tensorflow.keras as ks

from kgcnn.layers.casting import ChangeTensorType
from kgcnn.layers.gather import GatherNodesOutgoing
from kgcnn.layers.modules import DenseEmbedding, ActivationEmbedding, LazyAdd, OptionalInputEmbedding
from kgcnn.layers.mlp import GraphMLP, MLP
from kgcnn.layers.pooling import PoolingNodes, PoolingLocalEdges
from kgcnn.layers.pool.topk import PoolingTopK, UnPoolingTopK, AdjacencyPower
from kgcnn.utils.models import update_model_kwargs

# Graph U-Nets
# by Hongyang Gao, Shuiwang Ji
# https://arxiv.org/pdf/1905.05178.pdf

model_default = {'name': "Unet",
                 'inputs': [{'shape': (None,), 'name': "node_attributes", 'dtype': 'float32', 'ragged': True},
                            {'shape': (None,), 'name': "edge_attributes", 'dtype': 'float32', 'ragged': True},
                            {'shape': (None, 2), 'name': "edge_indices", 'dtype': 'int64', 'ragged': True}],
                 'input_embedding': {"node": {"input_dim": 95, "output_dim": 64},
                                     "edge": {"input_dim": 5, "output_dim": 64}},
                 'hidden_dim': {'units': 32, 'use_bias': True, 'activation': 'linear'},
                 'top_k_args': {'k': 0.3, 'kernel_initializer': 'ones'},
                 'activation': 'relu',
                 'use_reconnect': True,
                 'depth': 4,
                 'pooling_args': {"pooling_method": 'segment_mean'},
                 'gather_args': {"node_indexing": 'sample'},
                 'verbose': 10,
                 'output_embedding': 'graph',
                 'output_mlp': {"use_bias": [True, False], "units": [25, 1], "activation": ['relu', 'sigmoid']}
                 }


@update_model_kwargs(model_default)
def make_model(inputs=None,
               input_embedding=None,
               pooling_args=None,
               gather_args=None,
               top_k_args=None,
               depth=None,
               use_reconnect=None,
               hidden_dim=None,
               activation=None,
               name=None,
               verbose=None,
               output_embedding=None,
               output_mlp=None
               ):
    r"""Make U-Net graph network via functional API. Default parameters can be found in :obj:`model_default`.

    Args:
        inputs (list): List of dictionaries unpacked in :obj:`tf.keras.layers.Input`. Order must match model definition.
        input_embedding (dict): Dictionary of embedding arguments for nodes etc. unpacked in `Embedding` layers.
        depth (int): Number of graph embedding units or depth of the network.
        pooling_args (dict): Dictionary of layer arguments unpacked in `PoolingLocalEdges` layers.
        gather_args (dict): Dictionary of layer arguments unpacked in `GatherNodesOutgoing` layers.
        top_k_args (dict): Dictionary of layer arguments unpacked in `PoolingTopK` layers.
        use_reconnect (bool): Whether to use :math:`A^2` between pooling.
        hidden_dim (dict): Dictionary of layer arguments unpacked in hidden `Dense` layer.
        activation (dict, str): Activation to use.
        verbose (int): Level of verbosity.
        name (str): Name of the model.
        output_embedding (str): Main embedding task for graph network. Either "node", ("edge") or "graph".
        output_mlp (dict): Dictionary of layer arguments unpacked in the final classification `MLP` layer block.
            Defines number of model outputs and activation.

    Returns:
        tf.keras.models.Model
    """

    # Make input
    node_input = ks.layers.Input(**inputs[0])
    edge_input = ks.layers.Input(**inputs[1])
    edge_index_input = ks.layers.Input(**inputs[2])

    # embedding, if no feature dimension
    n = OptionalInputEmbedding(**input_embedding['node'],
                               use_embedding=len(inputs[0]['shape']) < 2)(node_input)
    ed = OptionalInputEmbedding(**input_embedding['edge'],
                                use_embedding=len(inputs[1]['shape']) < 2)(edge_input)
    edi = edge_index_input

    # Model
    n = DenseEmbedding(**hidden_dim)(n)
    in_graph = [n, ed, edi]
    graph_list = [in_graph]
    map_list = []

    # U Down
    i_graph = in_graph
    for i in range(0, depth):

        n, ed, edi = i_graph
        # GCN layer
        eu = GatherNodesOutgoing(**gather_args)([n, edi])
        eu = DenseEmbedding(**hidden_dim)(eu)
        nu = PoolingLocalEdges(**pooling_args)([n, eu, edi])  # Summing for each node connection
        n = ActivationEmbedding(activation=activation)(nu)

        if use_reconnect:
            ed, edi = AdjacencyPower(n=2)([n, ed, edi])

        # Pooling
        i_graph, i_map = PoolingTopK(**top_k_args)([n, ed, edi])

        graph_list.append(i_graph)
        map_list.append(i_map)

    # U Up
    ui_graph = i_graph
    for i in range(depth, 0, -1):
        o_graph = graph_list[i - 1]
        i_map = map_list[i - 1]
        ui_graph = UnPoolingTopK()(o_graph + i_map + ui_graph)

        n, ed, edi = ui_graph
        # skip connection
        n = LazyAdd()([n, o_graph[0]])
        # GCN
        eu = GatherNodesOutgoing(**gather_args)([n, edi])
        eu = DenseEmbedding(**hidden_dim)(eu)
        nu = PoolingLocalEdges(**pooling_args)([n, eu, edi])  # Summing for each node connection
        n = ActivationEmbedding(activation=activation)(nu)

        ui_graph = [n, ed, edi]

    # Output embedding choice
    n = ui_graph[0]
    if output_embedding == 'graph':
        out = PoolingNodes(**pooling_args)(n)
        out = ks.layers.Flatten()(out)  # will be dense
        main_output = MLP(**output_mlp)(out)
    elif output_embedding == 'node':
        out = GraphMLP(**output_mlp)(n)
        main_output = ChangeTensorType(input_tensor_type='ragged', output_tensor_type="tensor")(out)
    else:
        raise ValueError("Unsupported graph embedding for mode `Unet`")

    model = ks.models.Model(inputs=[node_input, edge_input, edge_index_input], outputs=main_output)
    return model
