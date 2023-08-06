def _check_type(sequence: list) -> str:
    type: str = ""

    for i in range(len(sequence) - 2):
        if sequence[i + 1] - sequence[i] == sequence[i + 2] - sequence[i + 1]:
            i += 1
            type = "arithmetic"
        elif sequence[i + 1] / sequence[i] == sequence[i + 2] / sequence[i + 1]:
            i += 1
            type = "geometric"
        else:
            return "tensor"

    return type


def _index_array(elements: list) -> list:
    result: list = []
    for i in range(len(elements)):
        result.append(i + 1)
    return result


def _predict_arithmetic(sequence: list, steps: int, d: float, verbose: bool) -> float:
    result: str = ""
    for i in range(steps):
        step: str = f"{sequence[0] + (len(sequence) + i) * d}, "
        if verbose:
            result += step
        else:
            result = step
    return result


def _predict_geometric(sequence: list, steps: int, r: float, verbose: bool) -> float:
    result: str = ""
    for i in range(steps):
        step: str = f"{sequence[0] * (pow(r, (len(sequence) + i)))}, "
        if verbose:
            result += step
        else:
            result = step
    return result


def _predict_tensor(sequence: list, steps: int, verbose: bool) -> str:
    import os
    os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
    os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

    from tensorflow import keras
    import numpy as np

    # creating model
    model: object = keras.Sequential(
        [keras.layers.Dense(units=1, input_shape=[1])])
    model.compile(optimizer="sgd", loss="mean_squared_error")

    # creating arrays
    indexes: list = np.array(_index_array(sequence), dtype=float)
    values: list = np.array(sequence, dtype=float)

    # training model
    model.fit(indexes, values, epochs=10000, verbose=0)

    # predicting
    result: str = ""
    for i in range(steps):
        prediction: float = model.predict([len(sequence) + (i + 1)])[0][0]
        prediction = format(prediction, ".1f")

        if verbose:
            result += f"{prediction}, "
        else:
            result = f"{prediction}, "

    return result


def predict(sequence: list, steps: int = 1, verbose: bool = False) -> str:
    if len(sequence) < 2:
        exit(1)

    # fixing sequence
    sequence = [float(x) for x in sequence]

    # getting sequence type
    sequence_type: str = _check_type(sequence)

    # predicting
    if sequence_type == "arithmetic":
        d = sequence[1] - sequence[0]
        result: str = _predict_arithmetic(sequence, steps, d, verbose)
    elif sequence_type == "geometric":
        r = sequence[1] / sequence[0]
        result: str = _predict_geometric(sequence, steps, r, verbose)
    else:
        result: str = _predict_tensor(sequence, steps, verbose)

    return result[:-2]
