import pandas as pd
import random
from marshmallow import Schema, ValidationError
import logging

from .fruits.model import data as fruits_data
from .fruits.model import model as fruits_model


class Source:

    """
    This needs to be passed just a string indictaing the source type,
    and the instance needs to grab the data and model from the right place
    using the pckg data...

    """

    def __init__(self, source):
        self.name = source
        if self.name == "fruits":
            self.model = fruits_model
        # logging.info(self.model)

        self.data = fruits_data
        # logging.info(self.data)

        self.new_data = []  # holding solution for the expanign choice issue

        self.process_passed_data()

        if not self.validate_data():
            raise ValueError(f"model to data validation error")

    def process_passed_data(self):
        """use pandas to comvert any passed data shape to a nice shape"""
        key_list = []

        for k in self.model.keys():
            if self.model[k]["stream"]["existing"]:
                key_list.append(k)

        columns = key_list

        df = pd.DataFrame(data=self.data, columns=columns)

        self.data = df.to_dict(orient="records")

    def create_data_schema(self):
        """create a marshmallow schema from passed model looking for data def only
        only therefore applies to data that exists in the data files, so can exlude
        existing: False

        """
        d = {}
        for k in self.model.keys():
            if self.model[k]["stream"]["existing"]:
                d.update({k: self.model[k]["field"]})

        DataSchema = Schema.from_dict(d)
        return DataSchema

    def validate_data(self):
        """
        use create marshmallow instance to validate passed data
        """

        DataSchema = self.create_data_schema()

        try:

            DataSchema(many=True).load(self.data)
            return True
        except ValidationError as e:
            logging.info(e)
            return False

    def new_event(self):
        """Once loaded, shaped and validated against the model this method can then be safely called

        the stream part of the model is defo going to need a schema validator: ie
        the actual generator types and setting needs a lot of work also
        if type == choice then default mut be list of len min 1 etc etc
        if exsiting == True, then must have field definition
        """

        new_event = {}

        for k in self.model.keys():

            field = self.model[k]["stream"]
            default = self.model[k]["stream"]["default"]
            if field["include"]:
                if field["type"] == "choice":
                    try:
                        new_event[k] = random.choice(self.data)[k]
                    except KeyError:
                        """handles where an event field not in the original data is being picked from"""
                        new_event[k] = random.choice(default)
                if field["type"] == "increment":
                    try:
                        new_event[k] = self.new_data[-1][k] + 1
                    except:
                        new_event[k] = default
                if field["type"] == "infer":
                    new_event[k] = "inference function called here"

        self.new_data.append(new_event)
        return new_event

    def set_field(self, data):
        """setter to add a new field to running source instance"""
        new_field = data["new_field"]
        self.model[new_field] = data["settings"]

        return "set_field complete"
