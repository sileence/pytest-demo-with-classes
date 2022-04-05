import pytest

class CannotConsumeElementError(Exception):
    pass

class Element:
    def __init__(self, name) -> None:
        self.name = name
        self.status = "inert"

    def generate(self):
        self.status = "strong"

    def wane(self):
        if self.status == "strong":
            self.status = "waning"
        elif self.status == "waning":
            self.status = "inert"

    def consume(self):
        if self.status == "inert":
            raise CannotConsumeElementError(f"Cannot consume {self.name} because it's not strong or waning")

        self.status = "inert"


class ElementTracker:
    def __init__(self) -> None:
        self.elements = {
            "fire": Element("Fire"),
            "ice": Element("Ice"),
            "air": Element("Air"),
            "earth": Element("Earth"),
            "light": Element("Light"),
            "dark": Element("Dark"),
        }

    def get(self, key):
        return self.elements.get(key)

    def generate(self, key):
        self.get(key).generate()

    def consume(self, key):
        self.get(key).consume()        

    def finishRound(self):
        for element in self.elements.values():
            element.wane()

def test_can_create_an_element():
    element = Element("Fire")
    assert "Fire" == element.name

    element = Element("Earth")
    assert "Earth" == element.name

def test_element_has_status_inert_by_default():
    element = Element("Fire")
    assert "inert" == element.status

def test_element_can_be_generated():
    element = Element("Fire")
    element.generate()
    assert "strong" == element.status

def test_element_can_wane():
    element = Element("Fire")
    element.generate()
    assert "strong" == element.status # sanity check

    element.wane()
    assert "waning" == element.status

    element.wane()
    assert "inert" == element.status

    element.wane()
    assert "inert" == element.status

def test_element_can_be_consumed_when_it_is_strong():
    element = Element("Fire")    
    element.generate()
    element.consume()
    assert "inert" == element.status

def test_element_can_be_consumed_when_it_is_waning():
    element = Element("Fire")    
    element.generate()
    element.wane()
    element.consume()
    assert "inert" == element.status

def test_element_cannot_be_consumed_when_it_is_inert():
    element = Element("Fire")    

    with pytest.raises(CannotConsumeElementError, match="Cannot consume Fire because it's not strong or waning"):
        element.consume()

def test_can_create_the_element_tracker_with_six_elements():
    tracker = ElementTracker()

    assert 6 == len(tracker.elements)

def test_can_get_an_element_from_the_element_tracker():
    tracker = ElementTracker()

    assert "Fire" == tracker.get("fire").name
    assert "Air" == tracker.get("air").name

def test_can_generate_an_element_from_the_element_tracker():
    tracker = ElementTracker()

    assert "inert" == tracker.get("fire").status # sanity check

    tracker.generate("fire")

    assert "strong" == tracker.get("fire").status

def test_can_consume_an_element_in_the_tracker():
    tracker = ElementTracker()
    tracker.generate("fire")
    tracker.consume("fire")

    assert "inert" == tracker.get("fire").status

def test_wane_the_elements_in_the_tracker_after_the_end_of_the_round():
    tracker = ElementTracker()
    tracker.generate("fire")
    tracker.generate("earth") # cragheart <3
    tracker.get("earth").wane()

    # Sanity checks:
    assert "strong" == tracker.get("fire").status
    assert "waning" == tracker.get("earth").status

    tracker.finishRound()

    assert "waning" == tracker.get("fire").status
    assert "inert" == tracker.get("earth").status
