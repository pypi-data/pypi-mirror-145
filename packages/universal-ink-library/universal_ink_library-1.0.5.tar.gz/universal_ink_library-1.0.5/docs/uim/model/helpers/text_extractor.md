Module uim.model.helpers.text_extractor
=======================================

Functions
---------

    
`uim_extract_text_and_semantics(uim_bytes: bytes, hwr_view: str = 'hwr', ner_view: Optional[str] = None) ‑> Tuple[List[dict], List[dict]]`
:   Extracting the text from Universal Ink Model.
    
    Parameters
    ----------
    uim_bytes: `bytes`
        Byte array with RIFF file from Universal Ink Model
    hwr_view: `str`
       HWR view.
    ner_view: `str`
        NER view if needed.
    
    Returns
    -------
    text: `List[dict]`
        List of text lines. Each line has its own dict containing the  bounding box, and all words
    entities.
    
    Raises
    ------
        `InkModelException`
            If the Universal Ink Model does not contain the view with the requested view name.

    
`uim_extract_text_and_semantics_from(ink_model: uim.model.ink.InkModel, hwr_view: str = 'hwr', ner_view: Optional[str] = None) ‑> Tuple[List[dict], List[dict]]`
:   Extracting the text from Universal Ink Model.
    
    Parameters
    ----------
    ink_model: InkModel -
        Universal Ink Model
    hwr_view: str -
       Name of the HWR view.
    ner_view: str -
        Name of the NER view if needed.
    
    Returns
    -------
    tuple(list of text lines (including bounding box), list knowledge uris)
    
    Raises
    ------
        `InkModelException`
            If the Universal Ink Model does not contain the view with the requested view name.
    
     Examples
    --------
    >>> from uim.codec.parser.uim import UIMParser
    >>> from uim.model.helpers.text_extractor import uim_extract_text_and_semantics_from
    >>> from uim.model.ink import InkModel
    >>> from uim.model.semantics.syntax import CommonViews, SEMANTIC_HAS_URI, SEMANTIC_HAS_LABEL, SEMANTIC_HAS_TYPE
    >>>
    >>> parser: UIMParser = UIMParser()
    >>> ink_model: InkModel = parser.parse('../ink/uim_3.1.0/2) Digital Ink is processable 1 (3.1 delta).uim')
    >>> if ink_model.has_knowledge_graph():
    >>>     #  Extract text lines and entities from model
    >>>     text_lines, entities = uim_extract_text_and_semantics_from(ink_model, hwr_view=CommonViews.HWR_VIEW.value,
    >>>                                                                ner_view=CommonViews.NER_VIEW.value)
    >>>     line_number: int = 1
    >>>     print('---------------------------------------------------------------------------------------------------')
    >>>     print(' Text lines:')
    >>>     print('---------------------------------------------------------------------------------------------------')
    >>>     for line in text_lines:
    >>>        print(f'{line_number}. Text line: {line["line"]} | {line["box"]}')
    >>>        word_num: int = 1
    >>>        for word in line['words']:
    >>>            print(f' {word_num}. Word: {word["word"]} | {word["box"]}')
    >>>            print(f'  -> Stroke UUIDs: {[str(w) for w in word["strokes"]]}')
    >>>            word_num += 1
    >>>        line_number += 1
    >>>     print()
    >>>     entity_number: int = 1
    >>>     print('---------------------------------------------------------------------------------------------------')
    >>>     print(' Entities:')
    >>>     print('---------------------------------------------------------------------------------------------------')
    >>>     for entity in entities:
    >>>         print(f'{entity_number}. URI: {entity["statements"][SEMANTIC_HAS_URI]} - '
    >>>               f'{entity["statements"][SEMANTIC_HAS_LABEL]} '
    >>>               f'({entity["statements"][SEMANTIC_HAS_TYPE]})')
    >>>         entity_number += 1