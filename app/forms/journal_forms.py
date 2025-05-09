from flask_wtf import FlaskForm
from flask_ckeditor import CKEditorField
from wtforms import StringField


class ArticleForm(FlaskForm):
    title = StringField("Title", validators=[...])
    content = CKEditorField("Content")
