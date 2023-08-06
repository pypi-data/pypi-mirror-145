Module uim.model.semantics.syntax
=================================

Classes
-------

`CommonRDF()`
:   Contains a list of used RDF types.

    ### Class variables

    `LOCALE: str`
    :

    `PRED_RDF_HAS_TYPE: str`
    :

`CommonViews(value, names=None, *, module=None, qualname=None, type=None, start=1)`
:   Contains a list of known ink model views.

    ### Ancestors (in MRO)

    * enum.Enum

    ### Class variables

    `CUSTOM_TREE`
    :

    `HWR_VIEW`
    :

    `LEGACY_HWR_VIEW`
    :

    `LEGACY_NER_VIEW`
    :

    `MAIN_INK_TREE`
    :

    `MAIN_SENSOR_TREE`
    :

    `NER_VIEW`
    :

    `SEGMENTATION_VIEW`
    :

`SegmentationSchema()`
:   UIM content segmentation schema prototype (generic).

    ### Class variables

    `BORDER: str`
    :

    `CONNECTOR: str`
    :

    `CORRECTION: str`
    :

    `DIAGRAM: str`
    :

    `DIAGRAM_CONNECTOR: str`
    :

    `DRAWING: str`
    :

    `DRAWING_ITEM: str`
    :

    `DRAWING_ITEM_GROUP: str`
    :

    `GARBAGE: str`
    :

    `LIST: str`
    :

    `LIST_ITEM: str`
    :

    `LIST_ITEM_BODY: str`
    :

    `MARKING: str`
    :

    `MARKING_TYPE_ENCIRCLING: str`
    :

    `MARKING_TYPE_PREDICATE: str`
    :

    `MARKING_TYPE_UNDERLINING: str`
    :

    `MATH_BLOCK: str`
    :

    `MATH_ITEM: str`
    :

    `MATH_ITEM_GROUP: str`
    :

    `SEGMENTATION_ROOT: str`
    :

    `TABLE: str`
    :

    `TEXT_LINE: str`
    :

    `TEXT_REGION: str`
    :

    `UNLABELLED: str`
    :

    `UNLABELLED_BLOCK: str`
    :

    `UNLABELLED_ITEM: str`
    :

    `UNLABELLED_ITEM_GROUP: str`
    :

    `WODL_CLASS_PREFIX: str`
    :

    `WORD: str`
    :

`SemanticTriple(subject: str, predicate: str, obj: str)`
:   SemanticTriple
    ==============
    A semantic triple, or simply triple, is the atomic data entity data model.
    As its name indicates, a triple is a set of three entities that codifies a statement about semantic data in the
    form of subject predicate object expressions.
    
    Parameters
    ----------
    subject: str
        Subject
    predicate: str
        Predicate
    obj: str
        Object

    ### Instance variables

    `object: str`
    :   Object of the statement. (`str`)

    `predicate: str`
    :   Predicate of the statement. (`str`)

    `subject: str`
    :   Subject of the statement. (`str`)

`Semantics()`
:   Contains types and entities that are used to store ontological knowledge definitions into the ink model's knowledge
    graph.

    ### Class variables

    `PRED_HAS_NAMED_ENTITY_DEFINITION: str`
    :

    `PRED_IS: str`
    :

    `TYPE: str`
    :

`TripleStore(triple_statements: List[uim.model.semantics.syntax.SemanticTriple] = None)`
:   TripleStore
    ===========
    
    Encapsulates a list of triple statements.
    
    Parameters
    ----------
    triple_statements: List[SemanticTriple]
        List of `SemanticTriple`s

    ### Instance variables

    `statements: List[uim.model.semantics.syntax.SemanticTriple]`
    :   List of triple statements. (`List[SemanticTriple]`)

    ### Methods

    `add_semantic_triple(self, subject: str, predicate: str, obj: str)`
    :   Adding a semantic triple
        :param subject: subject of the statement
        :param predicate: predicate of the statement
        :param obj: object of the statement

    `all_statements_for(self, subject: str, predicate: str = None) ‑> List[uim.model.semantics.syntax.SemanticTriple]`
    :   Returns all statements for a specific subject.
        
        Parameters
        ----------
        subject: `str`
            Filter for the subject URI
        predicate: `str`
            Predicate filter [optional]
        
        Returns
        -------
        statements: `List[SemanticTriple]`
            List of statements that match the filters.

    `append(self, triple_statement: uim.model.semantics.syntax.SemanticTriple)`
    :   Appending the triple statement.
        
        Parameters
        ----------
        triple_statement: SemanticTriple
            Triple that needs to be added

    `clear_statements(self)`
    :   Remove all statements.

    `determine_sem_type(self, node: InkNode, typedef_pred: str = 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type') ‑> Optional[str]`
    :   Determine the Semantic Type of node.
        
        Parameters
        ----------
        node: `InkNode`
            `InkNode` to extract the semantics from
        typedef_pred: `str`
            Predicate string
        
        Returns
        -------
        semantic_type: `str`
             Semantic type of the `InkNode`. None if the node is not found or the predicate statement.

    `filter(self, subject: Optional[str] = None, predicate: Optional[str] = None, obj: Optional[str] = None) ‑> List[uim.model.semantics.syntax.SemanticTriple]`
    :   Returns all statements for a specific subject.
        
        Parameters
        ----------
        subject: `Optional[str]`
            Filter for the subject URI [optional]
        predicate: `Optional[str]`
            Predicate filter [optional]
        obj: `Optional[str]`
            Object filter [optional]
        
        Returns
        -------
        statements: `List[SemanticTriple]`
            List of statements that match the filters.

    `remove_semantic_triple(self, triple: uim.model.semantics.syntax.SemanticTriple)`
    :   Removes a semantic triple from list.
        
        Parameters
        ----------
        triple: `SemanticTriple`
            Triple to be removed