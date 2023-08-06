# pyDOID
Python package with utilities for managing the Human Disease Ontology.

`pyDOID` was created to provide functionality that is currently unavailable (or difficult to create) in `DO.utils` the more extensive R package designed with the same purpose.

The functionality provided by `pyDOID` is encapsulated in three primary classes: 

1. The `DOrepo` class is designed specifically for access and manipulation of the Disease Ontology's git repository and the files within it. `DOrepo`:
    1. Inherits from the `git.repo.Repo` class and extends it with methods to check out individual tags, iteratively execute code across a range of tags, and to capture/restore the state of the git repo.
    2. Wraps the `pyDOID.owl` classes (outlined below) for specific files in the repository (`owl.functional`: doid-edit.owl; `owl.xml`: doid.owl and doid-merged.owl).
2. The `owl.functional` class provides a single method to extract class axioms from OWL files in the functional format. 
3. The `owl.xml` class provides methods to load and execute SPARQL queries against OWL files in the XML format.
