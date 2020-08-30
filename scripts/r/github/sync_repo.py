from _shutil import *


def print_help():
    print2("[h] help\n" "[c] commit\n" "[a] amend\n" "[p] push\n")


def commit(dry_run=False, amend=False):
    if dry_run:
        if get_output("git status --short").strip():
            call_echo("git add -A --dry-run")
    else:
        if not yes("Confirm?"):
            sys.exit(1)
        call_echo("git add -A")

        if amend:
            call_echo("git commit --amend --no-edit")
        else:
            call_echo('git commit -m "Initial commit"')


if __name__ == "__main__":
    repo_dir = r"{{GIT_REPO}}"
    repo_name = os.path.basename(repo_dir)

    cd(repo_dir)

    FNULL = fnull()
    ret = subprocess.call(
        "gh repo view rossning92/%s" % repo_name, shell=True, stdout=FNULL
    )
    if ret == 1:
        if not yes('Create "%s" on GitHub?' % repo_name):
            sys.exit(1)
        call_echo("gh repo create %s" % repo_name)

    # Init repo
    if not os.path.exists(".git"):
        call_echo("git init")
        call_echo(
            "git remote add origin https://github.com/rossning92/%s.git" % repo_name
        )

    # Add .gitignore
    if not os.path.exists(".gitignore"):
        with open(".gitignore", "w") as f:
            f.writelines(["/build"])

    print_help()
    while True:
        commit(dry_run=True)

        ch = getch()
        if ch == "h":
            print_help()
        elif ch == "c":
            commit()
        elif ch == "a":
            commit(amend=True)
        elif ch == "p":
            call_echo("git push -u origin master --force")
