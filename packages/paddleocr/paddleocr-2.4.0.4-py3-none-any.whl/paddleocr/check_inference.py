import numpy as np 
import paddle 

def verify_paddle_inference_correctness(layer, path, image_shape):
    from paddle import inference
    import numpy as np
    for i in range(len(image_shape)):
        if image_shape[i] < 0:
            image_shape[i] = 100
    model_file_path = path + ".pdmodel"
    params_file_path = path + ".pdiparams"
    config = inference.Config(model_file_path, params_file_path)
    config.enable_use_gpu(800, 0)
    predictor = inference.create_predictor(config)
    input_names = predictor.get_input_names()
    for name in input_names:
        input_tensor = predictor.get_input_handle(name)
    output_names = predictor.get_output_names()
    output_tensors = []
    for output_name in output_names:
        output_tensor = predictor.get_output_handle(output_name)
        output_tensors.append(output_tensor)
    x = np.random.random(size=tuple([1]+image_shape)).astype("float32")
    input_tensor.copy_from_cpu(x)
    predictor.run()
    prob_out = output_tensors[0].copy_to_cpu()

    layer.eval()
    pred = layer(paddle.to_tensor(x))
    correct = np.allclose(pred, prob_out, rtol=1e-4, atol=1e-4)
    absolute_diff = np.abs(pred.numpy() - prob_out)
    max_absolute_diff = np.max(absolute_diff)
    print("max_absolute_diff:", max_absolute_diff)
    assert correct, "Result diff when load and inference:\nlayer max_absolute_diff:{}"\
                  .format(max_absolute_diff)
    print("Successful, dygraph and inference predictions are consistent.")
