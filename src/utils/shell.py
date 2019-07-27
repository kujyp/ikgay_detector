import subprocess


def execute_with_message(statement):
    print("Execute... {}".format(statement))
    result = get_result_from_subprocess(statement)
    print("Done message=[{}]".format(result))


def get_result_from_subprocess(cmd):
    return (subprocess.check_output(cmd, shell=True)).decode("utf-8")


def get_statement_with_cd(path, statement):
    return "cd {} && {}".format(path, statement)
