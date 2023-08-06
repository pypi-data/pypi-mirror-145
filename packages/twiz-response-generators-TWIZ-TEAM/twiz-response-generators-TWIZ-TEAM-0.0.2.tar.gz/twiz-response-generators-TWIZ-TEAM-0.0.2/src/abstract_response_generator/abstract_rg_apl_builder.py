from typing import Optional, List

from cobot_core.apl.utils.documents.base_apl_document import BaseAplDocument
from cobot_core.apl.utils.documents.detail_apl_document import DetailAplDocument
from cobot_core.apl.utils.documents.image_list_apl_document import ImageListAplDocument
from cobot_core.apl.utils.documents.text_list_apl_document import TextListAplDocument
from cobot_core.apl.utils.items.image_list_item import ImageListItem
from cobot_core.apl.utils.items.text_detail_item import TextDetailItem
from cobot_core.apl.utils.items.text_list_item import TextListItem
from state_access.twiz_state import TwizState  # pip dependency

from twiz_cobot.modules.apl_screens import DetailAplWithVideo


class ResponseGeneratorAPLBuilder:
    twiz_state: TwizState
    apl_doc: BaseAplDocument

    def run(self, twiz_state: TwizState) -> Optional[List[dict]]:
        # will return an array with the built document and/or necessary directives
        self.twiz_state = twiz_state

        """
        # each RG will generate a different apl screen here calling the aux methods bellow.
        self.apl_doc = self._detail_document("Example RG APL Builder")  # Placeholder
        """
        return self.apl_doc.build_document()

    # ----- AUX METHODS TO CREATE APL DOCS ----- #
    def _make_apl_list_item_(self, primary_text: str, secondary_text: str, image_source: str = None) -> dict:
        if image_source:
            return {
                'primary_text': primary_text,
                'secondary_text': secondary_text,
                'image_source': image_source
            }
        else:
            return {
                'primary_text': primary_text,
                'secondary_text': secondary_text
            }

    # --- DETAIL DOCS --- #
    def _detail_document_(self, header_title: str, primary_text: str = None, secondary_text: str = None,
                          body_text: str = None, image_source: str = None) -> BaseAplDocument:
        detail_document = DetailAplDocument()
        detail_document.add_header_title(header_title)
        doc_item = self.__get_text_detail_item__(primary_text, secondary_text, body_text, image_source)
        detail_document.add_item(doc_item)
        return detail_document

    @staticmethod
    def __get_text_detail_item__(primary_text: str, secondary_text: str, body_text: str, image_source: str) \
            -> TextDetailItem:
        if image_source:
            doc_item = TextDetailItem(primary_text=primary_text,
                                      secondary_text=secondary_text,
                                      image_source=image_source, body_text=body_text)

        else:
            doc_item = TextDetailItem(primary_text=primary_text,
                                      secondary_text=secondary_text, body_text=body_text)
        return doc_item

    # --- KENBURNS DETAIL DOCS --- #
    def _kenburns_detail_document_(self, header_title: str, primary_text: str = None, secondary_text: str = None,
                                   body_text: str = None, image_source: str = None, ken_burns_video_url: str = None,
                                   thumbnail_img_url: str = None, is_blurred: bool = True) \
            -> BaseAplDocument:
        detail_document = DetailAplWithVideo()
        detail_document.add_header_title(header_title)

        detail_document.add_video_url(ken_burns_video_url)
        detail_document.add_thumbnail_img_url(thumbnail_img_url)
        detail_document.set_blurred_background(is_blurred)

        doc_item = self.__get_text_detail_item__(primary_text, secondary_text, body_text, image_source)
        detail_document.add_item(doc_item)
        return detail_document

    # --- IMAGE LIST DOCS --- #
    def _image_list_document_(self, header_title: str, item_list: List[dict]) -> BaseAplDocument:
        image_list_document = ImageListAplDocument()
        image_list_document.add_header_title(header_title)

        for item in item_list:  # Item structure: [item_primary_text, ]
            doc_item = self.__get_image_list_item__(item.get('primary_text', ''), item.get('secondary_text', None),
                                                    item.get('image_source', None))
            image_list_document.add_item(doc_item)
        return image_list_document

    @staticmethod
    def __get_image_list_item__(primary_text: str, secondary_text: str, image_source: str) \
            -> ImageListItem:
        if image_source:
            doc_item = ImageListItem(primary_text=primary_text, secondary_text=secondary_text,
                                     image_source=image_source)

        else:
            doc_item = ImageListItem(primary_text=primary_text, secondary_text=secondary_text)
        return doc_item

    # --- TEXT LIST DOCS --- #
    @staticmethod
    def _text_list_document_(header_title: str, item_list: List[dict]) -> BaseAplDocument:
        text_list_document = TextListAplDocument()
        text_list_document.add_header_title(header_title)

        for item in item_list:  # Item structure: [item_primary_text, ]
            doc_item = ResponseGeneratorAPLBuilder.__get_text_list_item__(item.get('primary_text', ''),
                                                                          item.get('secondary_text', None),
                                                                          item.get('image_source', None))
            text_list_document.add_item(doc_item)
        return text_list_document

    @staticmethod
    def __get_text_list_item__(primary_text: str, secondary_text: str, image_source: str) \
            -> TextListItem:
        if image_source:
            doc_item = TextListItem(primary_text=primary_text, secondary_text=secondary_text,
                                    image_source=image_source)
        else:
            doc_item = TextListItem(primary_text=primary_text, secondary_text=secondary_text)
        return doc_item
