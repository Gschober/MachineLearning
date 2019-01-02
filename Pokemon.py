from collections import namedtuple
import xml.etree.ElementTree as ET
from pprint import pprint
from math import pow
import heapq

def get_card_list():
    """
    You should never need to call this function!

    It parses an XML file containing statistics on every Pokemon
    card ever released, it then makes a list of Card objects to return.
    """
    tree = ET.parse("pokemon_cards.xml")
    root = tree.getroot()
    cards_xml = list(root[0])
    first_card_xml = cards_xml[0]
    tags = [e.tag for e in first_card_xml]
    Card = namedtuple('Card', tags)

    cards = []
    for card_xml in cards_xml:
        card = Card(*[e.text.strip() if e.text else None for e in card_xml])
        cards.append(card)
    return cards

# This is a global variable containing every Pokemon card.
# Indicies into this list represent instances of the respective card.
CARDS = get_card_list()


def default_value(card_index):
    """
    This function returns the monetary value of a given card index.
    """
    global CARDS
    card = CARDS[card_index]
    value = 0.01
    rarity_value_added = {
        'Common': 0,
        'Uncommon': 0.1,
        'Rare': 1,
        'Ultra-Rare': 10,
        'Promo': 0.2,
        'N/A': 0.15,
    }
    stage_value_added = {
        'Basic': 0.02,
        'Stage 1': 0.12,
        'Stage 2': 0.5,
        'Trainer': 0.67,
        'Supporter': 0.2,
        'Energy': 0.45,
        'Item': 0.98,
    }
    card_hp = int(card.hp) if card.hp else 0
    card_text =  3 * len(card.cardname)
    card_text += len(card.pokemonpower) if card.pokemonpower else 0
    card_text += len(card.attack1) if card.attack1 else 0
    card_text += len(card.attack2) if card.attack2 else 0
    card_text += len(card.attack3) * 10 if card.attack3 else 0
    card_text += len(card.attack4) * 20 if card.attack4 else 0

    value += rarity_value_added.get(card.rarity, 0)
    value += stage_value_added.get(card.rarity, 0)
    value += card_hp * 0.05
    value += card_text * 0.01
    return round(value, 4)


def misty_value(card_index):
    """
    This function returns the monetary value of a given card index.
    """
    global CARDS
    card = CARDS[card_index]
    value = default_value(card_index)
    value *= 0.66
    if 'Water' in card.type:
        value += 1
        value *= 3
    return round(value, 4)

def sabrina_value(card_index):
    """
    This function returns the monetary value of a given card index.
    """
    global CARDS
    card = CARDS[card_index]
    value = default_value(card_index)
    if 'Psychic' in card.type:
        value *= 2
    else:
        value *= 0.9
    return round(value, 4)

def jessie_value(card_index):
    """
    This function returns the monetary value of a given card index.
    """
    global CARDS
    card = CARDS[card_index]
    value = default_value(card_index)
    hp = int(card.hp) if card.hp else 100
    value *= pow((hp / 100), 3)
    return round(value, 4)


class Trainer:
    def __init__(self, name, value_function):
        self.name = name
        self.value_function = value_function



def get_minimum_needed_trades(trainers, decks):
    """
    Returns list of trades that results in everyone having no more mutually agreeable trades.
    Parameters:
        trainers: a list of Trainer instances
        decks: a list of indices into CARDS for each trainer
    """
    trades = []
    current = Node(decks)
    frontier = [current]
    while frontier != []:
        end=1
        current = frontier[0]
        i=0
        while i < len(current.decks):
            n = i+1
            while n < len(current.decks):
                if i!=n:
                    firstdeck = list(current.decks[i])
                    secdeck = list(current.decks[n])
                    for card in firstdeck:
                        for card2 in secdeck:
                            difme = trainers[i].value_function(card2) - trainers[i].value_function(card)
                            difother = trainers[n].value_function(card) - trainers[n].value_function(card2)
                            if difme > 0 and difother > 0:

                                #make trade in the deck
                                newdeck = list(current.decks)
                                trade1 = list(newdeck[i])
                                trade2 = list(newdeck[n])
                                trade1.remove(card)
                                trade2.remove(card2)
                                trade1.append(card2)
                                trade2.append(card)
                                newdeck[i]=tuple(trade1)
                                newdeck[n]=tuple(trade2)

                                #make new node and add to frontier
                                newnode = Node(newdeck)
                                newnode.parent = current
                                newnode.trade = [(card,trainers[i].name,card2,trainers[n].name)]
                                frontier.append(newnode)
                                end = 0
                n+=1
            i+=1
        frontier.remove(frontier[0])
        if end == 1:
            frontier = []
    while current.parent != None:
        trades += current.trade
        current = current.parent
    return trades

class Node:
    def __init__(self,decks):
        self.decks = decks
        self.parent = None
        self.trade = None
        self.sum=None
    def __lt__(self, other):
        return min(self.sum,other.sum)


def get_greedy_smallest_trades(trainers, decks):
    """
    Returns list of trades that results in everyone having no more mutually agreeable trades.
    Return the list of the smallest agreeable trades by greedy best-first search.
    Parameters:
        trainers: a list of Trainer instances
        decks: a list of indices into CARDS for each trainer
    """
    trades = []
    current = Node(list(decks))
    frontier =[]
    heapq.heappush(frontier,(-1,current))
    while frontier !=[]:
        end = 1
        current = heapq.heappop(frontier)[1]
        frontier=[]
        heapq.heapify(frontier)
        i = 0
        while i < len(current.decks):
            n = i + 1
            while n < len(current.decks):
                if i != n:
                    firstdeck = list(current.decks[i])
                    secdeck = list(current.decks[n])
                    for card in firstdeck:
                        for card2 in secdeck:
                            difme = trainers[i].value_function(card2) - trainers[i].value_function(card)
                            difother = trainers[n].value_function(card) - trainers[n].value_function(card2)
                            if difme > 0 and difother > 0:
                                # make trade in the deck
                                newdeck = list(current.decks)
                                trade1 = list(newdeck[i])
                                trade2 = list(newdeck[n])
                                trade1.remove(card)
                                trade2.remove(card2)
                                trade1.append(card2)
                                trade2.append(card)
                                newdeck[i] = tuple(trade1)
                                newdeck[n] = tuple(trade2)

                                # make new node and add to frontier
                                newnode = Node(newdeck)
                                newnode.parent = current
                                newnode.trade = [(card, trainers[i].name, card2, trainers[n].name)]
                                newnode.sum = SumCards(newdeck,trainers)-SumCards(current.decks,trainers)
                                heapq.heappush(frontier, (SumCards(newdeck,trainers)-SumCards(current.decks,trainers),newnode))
                                end=0

                n += 1
            i += 1
        if end == 1:
            frontier = []
    while current.parent != None:
        trades += current.trade
        current = current.parent
    trades.reverse()
    return trades

def SumCards(decks,trainers):
    i=0
    sum =0.0
    while i< len(decks):
        for card in decks[i]:
            sum+=trainers[i].value_function(card)
        i+=1
    return sum


if __name__ == "__main__":
    trainers = [Trainer('Myself', default_value), Trainer('Misty', misty_value)]

    decks = ((3521, 869, 5407, 5617, 2572, 753, 4039, 3307, 532),
             (5352, 3536, 3620, 1287, 554, 3985, 839, 729, 866))
    expected = [(4039, 'Myself', 1287, 'Misty'),
                (5617, 'Myself', 3536, 'Misty'),
                (3307, 'Myself', 3985, 'Misty'),
                (3521, 'Myself', 729, 'Misty'),
                (532, 'Myself', 866, 'Misty')]
    result = get_greedy_smallest_trades(trainers, decks)
    pprint(result)
    assert expected == result


