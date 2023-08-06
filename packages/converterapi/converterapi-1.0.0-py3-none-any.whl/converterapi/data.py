import json

class BaseData():
    def __init__(self, json_dict):
        self.json_dict = json_dict

    def to_json(self):
        return json.dumps(self.json_dict)

class Task(BaseData):
    '''
        - uuid: [string] unique task identifier.
        - created_at: [string] date time string in UTC.
        - modified_at: [string] date time string in UTC.
        - identifier_uuid: [string] unique model identifier for converter server users.
        - model_url: [string] model's download url.
        - model_type: [string] type of model. (ex: tflite-postcalibration, tflite-edgetpu)
        - callback_url: [string] every time when there is task status update, 
                the converter server will send the task status json object to the given url.
        - complete_upload_url: [string] model's upload url.
        - status: [string] task status (waiting, downloading, compiling, converted, cancelled). 
                cancelled means there is an error occurred.
        - log: [string] converter log
        - compiler_version: [string] compiler version used to compile the model.
        - compiler_type: [string] compiler type used to compile the model.
        - compiler_option: [string] compiler option used to compile the model.
        - task_models_key_by: [Model] converted model's information.
    '''
    def __init__(self, task_data):
        super().__init__(task_data)
        self.uuid = task_data.get("uuid", None)
        self.created_at = task_data.get("created_at", None)
        self.modified_at = task_data.get("modified_at", None)
        self.identifier_uuid = task_data.get("identifier_uuid", None)
        self.model_url = task_data.get("model_url", None)
        self.model_type = task_data.get("model_type", None)
        self.callback_url = task_data.get("callback_url", None)
        self.complete_upload_url = task_data.get("complete_upload_url", None)
        self.status = task_data.get("status", None)
        self.log = task_data.get("log", None)
        self.compiler_version = task_data.get("compiler_version", None)
        self.compiler_type = task_data.get("compiler_type", None)
        self.compiler_option = task_data.get("compiler_option", None)
        self.task_models_key_by = Model(task_data.get("task_models_key_by", None)) if task_data.get("task_models_key_by", None) is not None else None

class Model(BaseData):
    '''
        - uuid: [string] unique model identifier
        - created_at: [string] date time string in UTC.
        - modified_at: [string] date time string in UTC.
        - task_uuid: [string] unique task identifier.
        - upload_url: [string] Server path to which the model was uploaded.
        - upload_time: [string] date time string in UTC.
        - is_deleted: [bool] bool value for whether the model was deleted.
    '''
    def __init__(self, model_data):
        super().__init__(model_data)
        self.uuid = model_data.get("uuid", None)
        self.created_at = model_data.get("created_at", None)
        self.modified_at = model_data.get("modified_at", None)
        self.task_uuid = model_data.get("task_uuid", None)
        self.upload_url = model_data.get("upload_url", None)
        self.upload_time = model_data.get("upload_time", None)
        self.is_deleted = model_data.get("is_deleted", None)

class Version(BaseData):
    '''
        - compiler: [string] compiler type.
        - images: [Image] docker information
    '''
    def __init__(self, version_data):
        super().__init__(version_data)
        self.compiler = version_data.get("compiler", None)
        images = []
        if version_data.get("images", None) is not None:
            for i in range(0, len(version_data["images"])):
                images.append(Image(version_data["images"][i]))
        else:
            images = None
        self.images = images

class Image(BaseData):
    '''
        - tag: [string] compiler version. (same as docker tag)
        - upload_date: [string] date time string in UTC.
    '''
    def __init__(self, image_data):
        super().__init__(image_data)
        self.tag = image_data.get("tag", None)
        self.upload_date = image_data.get("upload_date", None)

class Option(BaseData):
    '''
        - required: [string] required parameter for compiler
        - optional: [string] optional parameter for compiler
    '''
    def __init__(self, option_data):
        super().__init__(option_data)
        required = []
        if option_data.get("required", None) is not None:
            for i in range(0, len(option_data["required"])):
                required.append(option_data["required"][i])
        else:
            required = None
        self.required = required

        optional = []
        if option_data.get("optional", None) is not None:
            for i in range(0, len(option_data["optional"])):
                optional.append(option_data["optional"][i])
        else:
            optional = None
        self.optional = optional