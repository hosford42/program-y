import xml.etree.ElementTree as ET

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.topicstar import TemplateTopicStarNode
from programy.dialog import Conversation, Question
from programy.parser.pattern.matcher import MatchContext, Match
from programy.parser.pattern.nodes.oneormore import PatternOneOrMoreWildCardNode

from test.parser.template.base import TemplateTestsBaseClass


class TemplateNodeTests(TemplateTestsBaseClass):

    def test_to_str_defaults(self):
        node = TemplateTopicStarNode()
        self.assertEquals("TOPICSTAR", node.to_string())

    def test_to_str_no_defaults(self):
        node = TemplateTopicStarNode(index=2)
        self.assertEquals("TOPICSTAR index=2", node.to_string())

    def test_to_xml_defaults(self):
        root = TemplateNode()
        node = TemplateTopicStarNode()
        root.append(node)

        xml = root.xml_tree(self.bot, self.clientid)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual("<template><topicstar /></template>", xml_str)

    def test_to_xml_no_defaults(self):
        root = TemplateNode()
        node = TemplateTopicStarNode(index=3)
        root.append(node)

        xml = root.xml_tree(self.bot, self.clientid)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual('<template><topicstar index="3" /></template>', xml_str)

    def test_resolve_with_defaults_inside_topic(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateTopicStarNode()
        self.assertIsNotNone(node)
        self.assertEquals(1, node.index)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        conversation = Conversation("testid", self.bot)

        question = Question.create_from_text("Hello world")
        question.current_sentence()._response = "Hello matey"
        conversation.record_dialog(question)

        question = Question.create_from_text("How are you")
        question.current_sentence()._response = "Very well thanks"
        conversation.record_dialog(question)

        match = PatternOneOrMoreWildCardNode("*")
        context = MatchContext(max_search_depth=100, max_search_timeout=-1)
        context.add_match(Match(Match.TOPIC, match, "Matched"))
        question.current_sentence()._matched_context = context
        conversation.record_dialog(question)

        self.bot._conversations["testid"] = conversation

        self.assertEquals("Matched", root.resolve(self.bot, "testid"))

    def test_resolve_no_defaults_inside_topic(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateTopicStarNode(index=1)
        self.assertIsNotNone(node)
        self.assertEqual(1, node.index)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        conversation = Conversation("testid", self.bot)

        question = Question.create_from_text("Hello world")
        question.current_sentence()._response = "Hello matey"
        conversation.record_dialog(question)

        question = Question.create_from_text("How are you")
        question.current_sentence()._response = "Very well thanks"
        conversation.record_dialog(question)

        match = PatternOneOrMoreWildCardNode("*")
        context = MatchContext(max_search_depth=100, max_search_timeout=-1)
        context.add_match(Match(Match.TOPIC, match, "Matched"))
        question.current_sentence()._matched_context = context
        conversation.record_dialog(question)

        self.bot._conversations["testid"] = conversation

        self.assertEqual("Matched", node.resolve(self.bot, "testid"))
