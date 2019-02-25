import os
import tempfile
import subprocess
import json


use_filetypes = [".py", ".txt", ".md", ".js"]
devnull = open(os.devnull, 'w')


class GitCommands:
    @staticmethod
    def files_in_commit(commit_id):
        return [s.strip() for s in
                subprocess.check_output("git diff-tree --no-commit-id --name-only -r {}".format(commit_id),
                                        shell=True).decode().split('\n')]

    @staticmethod
    def last_n_commits(n):
        return subprocess.check_output('git log --format="%H" -n {}'.format(n), shell=True).decode().split('\n')

    @staticmethod
    def all_commits():
        return GitCommands.last_n_commits(100000)

    @staticmethod
    def commit_message(commit_id):
        return subprocess.check_output("git log --format=%B -n 1 {}".format(commit_id), shell=True).decode()

    @staticmethod
    def file_content(commit_id, filename):
        try:
            return subprocess.check_output("git show {}:{}".format(commit_id, filename), shell=True, stderr=devnull).decode()
        except subprocess.CalledProcessError as e:
            return None


class Commit:
    def __init__(self, filename, content_before, content_after, commit_id, commit_message):
        self.content_before = content_before
        self.content_after = content_after
        self.commit_id = commit_id
        self.commit_message = commit_message
        self.filename = filename

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return str(self.__dict__)


def get_histories(github_repo_urls, use_filetypes=use_filetypes):
    commits = []
    for url in github_repo_urls:
        print("Processing repo @ {}.".format(url))
        with tempfile.TemporaryDirectory() as dirpath:
            os.chdir(dirpath)
            os.system("git clone {}".format(url))
            project_name = subprocess.check_output("ls", shell=True, stderr=devnull).decode().strip()
            os.chdir(project_name)
            commit_ids = GitCommands.all_commits()
            n_commits = len(commit_ids)
            print("Processing {} commits.".format(len(commit_ids)))
            commit_messages = [GitCommands.commit_message(i) for i in commit_ids]
            i = 0

            while i + 1 < len(commit_ids):
                print("\rCommit {}/{}.".format(i, n_commits), end='')
                commit_id_before = commit_ids[i + 1]
                commit_id = commit_ids[i]
                files = GitCommands.files_in_commit(commit_id)
                for file in files:
                    if not any([file.endswith(filetype) for filetype in use_filetypes]):
                        continue
                    content_before = GitCommands.file_content(commit_id_before, file)
                    if content_before is not None:
                        content = GitCommands.file_content(commit_id, file)
                        if content is not None:
                            commits.append(Commit(file, content_before, content, commit_id, commit_messages[i]))
                i += 1

    return commits


if __name__ == '__main__':
    pass


