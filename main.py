from subprocess import call
import bin.helper


"""
This script acts as the glue to automate the steps of creating the training/testing files for neural network training, training and testing a neural network, and creating the necessary files for integration with RuNNer++

In particular, this script activates the files given in the main.info file, particularly the createTT, trainNN, and testNN files.  This script provides each of these files with a link to the appropriate info files as follows:

... [createTT].extension [ttInfo] [symmInfo] [nnInfo]
... [*NN].extension [ttInfo] [nnInfo]

This script expects that createTT will create all necessary files in the appropriate runner directory except input.nn and input.nn.RuNNer++.  These two files are the responsibility of either [trainNN] or [translateNN].

For details on the main.info file which guides the use of this script, please examine the main.info included with this package.

Written by @Checkmate
"""


def execute_file(data, filename, args, verbose=False):
    """
    Given a filename and arguments 'args'
    Attempts to execute that file with the given arguments
    Raises a ValueError if the file extension is not supported
    """
    if filename.endswith(".py"):
        if verbose:
            bin.helper.print_info("python " + filename + " " + " ".join(args))
        e = call([data["python"], filename] + args)
    elif filename.endswith(".lua"):
        if verbose:
            bin.helper.print_info("th " + filename + " " + " ".join(args))
        e = call([data["torch"], filename] + args)
    else:
        bin.helper.print_error(filename + " not run (unrecognized file type)")
        exit()
    if e != 0:
        bin.helper.print_error("Fatal error!  Exiting")
        exit()


def main():
    expected = ["createTT", "trainNN", "testNN", "ttInfo", "symmInfo", "nnInfo"]
    defaults = {"createNewTT" : True, "createNewNN" : True, "testOnly" : False, "runTests" : True, "verbose" : False}
    files = bin.helper.get_data("main.info", expected, defaults)
    if not files["testOnly"]:
        if files["createNewTT"]:
            execute_file(files["createTT"], [files["ttInfo"], files["symmInfo"], files["nnInfo"]], verbose=files["verbose"])
        if files.has_key("createNN"):
            execute_file(files["createNN"], [files["ttInfo"], files["nnInfo"]], verbose=files["verbose"])
        execute_file(files["trainNN"], [files["ttInfo"], files["nnInfo"]], verbose=files["verbose"])
        if files.has_key("translateNN"):
            execute_file(files["translateNN"], [files["nnInfo"]], verbose=files["verbose"])
    if files["runTests"]:
        execute_file(files["testNN"], [files["ttInfo"], files["nnInfo"]], verbose=files["verbose"])
    if files["verbose"]:
        bin.helper.print_info("Exiting main.py")

if __name__ == "__main__":
    main()

    
