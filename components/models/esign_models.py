# coding:utf-8
"""eSign Database Module"""
import enum

from sqlalchemy import (CHAR, Column, Enum, Integer, SmallInteger, String,
                        Text, UniqueConstraint)
from sqlalchemy.ext.declarative import declarative_base

BASE = declarative_base()

# turn to dict
BASE.to_dict = lambda self: dict(
    [
        (key, self.__dict__[key])
        for key in self.__dict__
        if not key.startswith('_')
    ])
# turn to string
BASE.__repr__ = lambda self: self.__tablename__ + ' => ' + str(self.to_dict())


class User(BASE):
    """User model"""
    __tablename__ = 'user'

    user_id = Column(CHAR(36), primary_key=True)
    ws_id = Column(Integer, default=0, index=True)
    old_ws_id = Column(Integer, default=0, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    active_code = Column(CHAR(32))
    expire_time = Column(Integer, nullable=False, default=0, index=True)
    register_time = Column(Integer, default=0, index=True)
    appear_time = Column(Integer, nullable=False, index=True)
    active_status = Column(SmallInteger, nullable=False, default=0)
    valid = Column(SmallInteger, nullable=False)
    permission = Column(SmallInteger, nullable=False)
    first_name = Column(String(255))
    last_name = Column(String(255))
    company = Column(String(255))
    title = Column(String(255))
    country = Column(CHAR(40))
    avatar = Column(CHAR(180))
    company_logo = Column(CHAR(180))

    __table_args__ = ({'mysql_engine': 'InnoDB'}, )


class File(BASE):
    """File model"""
    __tablename__ = 'file'

    class TypeEnum(enum.Enum):
        """File type enum class"""
        upload = 1
        cloud = 2
        sign_complete = 3

    file_id = Column(CHAR(24), primary_key=True)
    user_id = Column(CHAR(36), index=True, nullable=False)
    file_name = Column(String(255), nullable=False)
    file_size = Column(Integer, nullable=False)
    total_pages = Column(SmallInteger, nullable=False)
    file_type = Column(Enum(TypeEnum), nullable=False)
    valid = Column(SmallInteger, nullable=False)
    create_time = Column(Integer, nullable=False, index=True)

    __table_args__ = ({'mysql_engine': 'InnoDB'}, )


class SignFlow(BASE):
    """Signflow model"""
    __tablename__ = 'signflow'

    #     initiated = 1
    #     prepared = 2
    #     sent = 3
    #     signing = 4
    #     completed = 5

    # notice level:
    # 0: all notice
    # 1: signed and completed notice
    # 2: completed notice
    # 3: no notice

    flow_id = Column(CHAR(24), primary_key=True)
    user_id = Column(CHAR(36), nullable=True, index=True)
    logo = Column(CHAR(180))
    origin_file = Column(CHAR(24), nullable=False, index=True)
    subject = Column(String(255))
    message = Column(Text)
    valid = Column(SmallInteger, nullable=False)
    access_code = Column(CHAR(18))
    notice_level = Column(SmallInteger, default=0)
    initiate_time = Column(Integer, nullable=False, index=True)

    __table_args__ = ({'mysql_engine': 'InnoDB'}, )


class Flower(BASE):
    """Flower model"""
    __tablename__ = 'flower'

    flower_id = Column(CHAR(36), primary_key=True)
    flow_id = Column(CHAR(24), nullable=False, index=True)
    user_id = Column(CHAR(36), index=True)
    email = Column(String(255), nullable=False, index=True)
    role = Column(Integer, nullable=False, default=0)
    order = Column(SmallInteger, default=0)
    signed = Column(SmallInteger, default=0)
    subject = Column(String(255))
    message = Column(Text)
    refuse_notice = Column(SmallInteger, default=0)
    update_time = Column(Integer, nullable=False, index=True)

    __table_args__ = (UniqueConstraint(
        'flow_id', 'email', name='uix_flower_flow_id_email'), {
            'mysql_engine': 'InnoDB'
        }, )


class SignFlowRecord(BASE):
    """Signflow record model"""
    __tablename__ = 'signflow_record'

    class ActionEnum(enum.Enum):
        """Action enum class"""
        initiated = 1
        prepared = 2
        sent = 3
        agreement = 4
        viewed = 5
        signed = 6
        downloaded = 7
        completed = 8

    record_id = Column(Integer, primary_key=True)
    flow_id = Column(CHAR(36), nullable=False, index=True)
    action = Column(Enum(ActionEnum), nullable=False)
    operate_user = Column(CHAR(36), nullable=False, index=True)
    operate_email = Column(CHAR(120), nullable=False, index=True)
    operate_ip = Column(CHAR(17), nullable=False)
    operate_time = Column(Integer, nullable=False, index=True)

    __table_args__ = (UniqueConstraint(
        'flow_id', 'operate_email', 'action',
        name='uix_sign_flow_record_flow_id_email_action'), {
            'mysql_engine': 'InnoDB'
        }, )


class Position(BASE):
    """Position model"""
    __tablename__ = 'position'

    class SignTypeEnum(enum.Enum):
        """Sign type enum class"""
        text = 1
        image = 2

    class PosTypeEnum(enum.Enum):
        """Position type enum class"""
        fullname = 1
        initial = 2
        date = 11
        title = 12
        company = 13
        custom = 14

    pos_id = Column(CHAR(36), primary_key=True)
    pos_flow = Column(CHAR(36), nullable=False, index=True)
    pos_params = Column(Text, nullable=False)
    pos_type = Column(Enum(PosTypeEnum))
    pos_setor = Column(CHAR(36), nullable=False, index=True)
    pos_signer = Column(CHAR(36), nullable=False, index=True)
    set_time = Column(Integer, default=0, index=True)
    sign_type = Column(Enum(SignTypeEnum))
    sign_content = Column(String(255))
    sign_time = Column(Integer, default=0, index=True)
    sign_ip = Column(CHAR(17), default='0.0.0.0')

    __table_args__ = ({'mysql_engine': 'InnoDB'}, )


class Template(BASE):
    """Template model"""
    __tablename__ = 'template'

    template_id = Column(CHAR(36), primary_key=True)
    user_id = Column(CHAR(36), nullable=False, index=True)
    file_id = Column(CHAR(24), nullable=False, index=True)
    valid = Column(SmallInteger, nullable=False)

    __table_args__ = ({'mysql_engine': 'InnoDB'}, )


class TemplatePos(BASE):
    """Template position model"""
    __tablename__ = 'template_position'

    template_pos_id = Column(CHAR(36), primary_key=True)
    template_id = Column(CHAR(36), nullable=False, index=True)
    template_pos_params = Column(Text, nullable=False)
    valid = Column(SmallInteger, nullable=False)

    __table_args__ = ({'mysql_engine': 'InnoDB'}, )


class Signature(BASE):
    """Sign image model"""
    __tablename__ = 'sign_image'

    class ImageTypeEnum(enum.Enum):
        """Signature type enum class"""
        fullname = 1
        initial = 2

    signature_id = Column(CHAR(36), primary_key=True)
    user_id = Column(CHAR(36), nullable=False, index=True)
    image_type = Column(Enum(ImageTypeEnum), nullable=False)
    path = Column(Text)
    valid = Column(SmallInteger, default=1)
    time = Column(Integer, default=0)

    __table_args__ = ({'mysql_engine': 'InnoDB'}, )
