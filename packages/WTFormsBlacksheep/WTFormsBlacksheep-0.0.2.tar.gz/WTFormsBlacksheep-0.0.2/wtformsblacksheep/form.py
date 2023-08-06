import asyncio
from dataclasses import is_dataclass, asdict
from typing import Any

from blacksheep.messages import Request
from multidict import MultiDict
from pydantic import BaseModel
from wtforms import Form, ValidationError

__all__ = ['BlacksheepForm']

SUBMIT_METHODS = {'POST', 'PUT', 'PATCH', 'DELETE'}
_Auto = object()


class BlacksheepForm(Form):
    def __init__(self, request: Request, *args, **kwargs):
        # cache request
        self._request = request

        super().__init__(*args, **kwargs)

    @classmethod
    async def from_formdata(
            cls,
            request: Request,
            formdata: Any = None,
            **kwargs
    ):
        if formdata is None:
            if request.method in SUBMIT_METHODS:
                form = await request.form()
                formdata = MultiDict(form)
        else:
            if is_dataclass(formdata):
                formdata = MultiDict(asdict(formdata))
            elif issubclass(type(formdata), BaseModel):
                formdata = MultiDict(formdata.dict())
            elif isinstance(formdata, dict):
                formdata = MultiDict(formdata)
            else:
                raise ValueError(f"{type(formdata)} is not supported for formdata")

        # return new instance
        return cls(request, formdata=formdata, **kwargs)

    async def _validate_async(self, validator, field):
        try:
            await validator(self, field)
        except ValidationError as e:
            field.errors.append(e.args[0])
            return False
        return True

    async def validate(self, extra_validators=None):
        if extra_validators is not None:
            extra = extra_validators.copy()
        else:
            extra = {}

        async_validators = {}

        # use extra validators to check for StopValidation errors
        completed = []

        def record_status(form, field):
            completed.append(field.name)

        for name, field in self._fields.items():
            func = getattr(self.__class__, f"async_validate_{name}", None)
            if func:
                async_validators[name] = (func, field)
                extra.setdefault(name, []).append(record_status)

        # execute non-async validators
        success = super().validate(extra_validators=extra)

        # execute async validators
        tasks = [self._validate_async(*async_validators[name]) for name in completed]
        async_results = await asyncio.gather(*tasks)

        # check results
        if False in async_results:
            success = False

        return success

    def is_submitted(self):
        """Consider the form submitted if there is an active request and
        the method is ``POST``, ``PUT``, ``PATCH``, or ``DELETE``.
        """
        return self._request.method in SUBMIT_METHODS

    async def validate_on_submit(self, extra_validators=None):
        return self.is_submitted() and await self.validate(extra_validators=extra_validators)
