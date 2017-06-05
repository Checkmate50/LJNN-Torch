from subprocess import call
from bin.helper import get_data


def execute_file(filename, args, verbose=False):
    """
    Given a filename and arguments 'args'
    Attempts to execute that file with the given arguments
    Raises a ValueError if the file extension is not supported
    """
    if filename.endswith(".py"):
        if verbose:
            print("python " + filename + " " + " ".join(args))
        call(["python", filename] + args)
    elif filename.endswith(".lua"):
        if verbose:
            print("th " + filename + " " + " ".join(args))
        call(["th", filename] + args)
    else:
        raise ValueError(filename + " not run (unrecognized file type)")


def main():
    expected = ["createTT", "createNN", "trainNN", "testNN", "ttInfo", "symmInfo", "nnInfo"]
    defaults = {"createNewTT" : True, "testOnly" : False, "noTest" : False, "verbose" : False}
    files = get_data("main.info", expected, defaults)
    if not files["testOnly"]:
        if files["createNewTT"]:
            execute_file(files["createTT"], [files["ttInfo"], files["symmInfo"]], verbose=files["verbose"])
            return
        execute_file(files["createNN"], [files["nnInfo"]], verbose=files["verbose"])
        execute_file(files["trainNN"], [files["ttInfo"], files["nnInfo"]], verbose=files["verbose"])
    if not files["noTest"]:
        execute_file(files["testNN"], [files["ttInfo"], files["nnInfo"]], verbose=files["verbose"])
    if files["verbose"]:
        print("Exiting main.py")

if __name__ == "__main__":
    main()

    
