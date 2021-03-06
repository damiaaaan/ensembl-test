from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.exceptions import HTTPException
from config import Config
from errors import error_response

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)


gene_autocomplete = db.Table('gene_autocomplete', db.metadata, autoload=True, autoload_with=db.engine)


@app.errorhandler(HTTPException)
def handle_exception(e):
    return error_response(e.code, e.description)


def make_search(species, query, limit):
    search = "%{}%".format(query)
    result = db.session.query(gene_autocomplete) \
        .filter(gene_autocomplete.c.species == species) \
        .filter(gene_autocomplete.c.display_label.like(search)) \
        .group_by(gene_autocomplete.c.display_label) \
        .limit(limit) \
        .all()
    return result


@app.route('/gene_suggest', methods=['GET'])
def gene_suggest():
    species = request.args.get('species')
    query = request.args.get('query')
    limit = request.args.get('limit', 10, type=int)

    if not species or species == '':
        return error_response(400, 'Missing parameter')

    if limit <= 0:
        return error_response(400, 'Wrong parameter value')

    result = make_search(species, query, limit)

    data = []
    for (i, r) in enumerate(result):
        data.append({i: r.display_label})

    return jsonify({'gene_names': data})


if __name__ == '__main__':
    app.run(host="0.0.0.0")
