"""Repository management for the Human Disease Ontology."""

import os
from git import Repo
from tqdm import tqdm

from . import owl, util


def restore_head_dec(function):
    def _rh_inner(self, *args, **kwargs):
        if self.head.is_detached:
            initial_head = self.head.commit
        else:
            initial_head = self.head.ref
        func = function(self, *args, **kwargs)
        self.git.checkout(initial_head)
        return func
    return _rh_inner


def capture_head(repo):
    if not isinstance(repo, pyDOID.repo.Repo):
        raise TypeError("repo must be a pyDOID.repo.Repo")
    if repo.head.is_detached:
        captured_head = repo.head.commit
    else:
        captured_head = repo.head.ref
    return captured_head


def checkout_tag(repo, tag_name):
    if not isinstance(repo, pyDOID.repo.Repo):
        raise TypeError("repo must be a pyDOID.repo.Repo")
    for t in repo.tags:
        if t.name == tag_name:
            repo.git.checkout(t)
            return t.name
    # MUST fail if tag is not found
    raise ValueError("tag_name does not correspond to any tags in repo.")


def query_release(repo, file, release, query):
    if not isinstance(repo, pyDOID.repo.Repo):
        raise TypeError("repo must be a pyDOID.repo.Repo")
    checkout_tag(repo, tag_name=release)
    o = pyDOID.owl.xml(file)
    res = o.query(query)
    return res


class DOrepo(Repo):
    """A class for the Human Disease Ontology repository."""

    def __init__(self, path):
        super().__init__(util.ensure_dir(path))
        self.path = os.path.dirname(self.git_dir)
        self._onto_dir = os.path.join(self.path, "src", "ontology")
        self.doid_edit = owl.functional(os.path.join(self._onto_dir, "doid-edit.owl"))
        self.doid = owl.xml(os.path.join(self._onto_dir, "doid.owl"))
        self.doid_merged = owl.xml(os.path.join(self._onto_dir, "doid-merged.owl"))

    @restore_head_dec
    def tag_iterate(self, fxn, start=None, end=None, *args, **kwargs):
        tags = sorted(self.tags, key=lambda t: t.commit.committed_datetime)
        t_name = [t.name for t in tags]
        if start is None:
            start = t_name[0]
        if end is None:
            end = t_name[-1]

        res = {}
        include = False
        tag_it = tqdm(
            tags[t_name.index(start):(t_name.index(end) + 1)],
            desc="executing at...",
            unit="tag"
        )
        for t in tag_it:
            self.git.checkout(t)
            res[t.name] = fxn(*args, **kwargs)

        return res

    def capture_head(self):
        if self.head.is_detached:
            self.captured_head = self.head.commit
        else:
            self.captured_head = self.head.ref
        return self.captured_head

    def restore_head(self):
        res = self.git.checkout(self.captured_head)
        return res

    def checkout_tag(self, tag_name):
        for t in self.tags:
            if t.name == tag_name:
                self.git.checkout(t)
                return t.name
        # MUST fail if tag is not found
        raise ValueError("tag_name does not correspond to any tags in the repo.")
