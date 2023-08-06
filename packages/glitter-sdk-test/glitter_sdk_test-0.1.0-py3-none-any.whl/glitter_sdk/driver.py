# Copyright GlitterClient GmbH and GlitterClient contributors
# SPDX-License-Identifier: (Apache-2.0 AND CC-BY-4.0)
# Code is Apache-2.0 and docs are CC-BY-4.0

from .transport import Transport
from .utils import normalize_nodes

class GlitterClient:
    """A :class: `~driver.GlitterClient` is python client  for glitter. It can be connect, create schema, put docs and search .

    """

    def __init__(self, *nodes, headers=None, transport_class=Transport, timeout=20):
        """Initialize a :class:`~driver.GlitterClient` driver instance.

        Args:
            *nodes:(list of (str or dict)): Glitter nodes to connect to.
            headers (dict): Optional headers that will be passed with each request
            transport_class: Optional transport class to use.
            timeout (int): Optional timeout in seconds that will be passed to each request.
        """
        self._headers = headers
        self._nodes = normalize_nodes(*nodes, headers=headers)
        self._transport = transport_class(*self._nodes, timeout=timeout)
        self._db = DataBase(self)
        self._chain = Chain(self)
        self._admin = Admin(self)
        self.api_prefix = '/v1'

    @property
    def nodes(self):
        """:obj:`tuple` of :obj:`str`:
         URLs of connected nodes.
        """
        return self._nodes

    @property
    def transport(self):
        """:class:`~driver.Transport`: Object responsible for forwarding requests to a :class:`~driver.Connection` instance (node).
        """
        return self._transport

    @property
    def chain(self):
        """:class:`~driver.Chain`: query block or transaction info.
        """
        return self._chain

    @property
    def admin(self):
        """:class:`~driver.Admin`: Exposes functionalities of the ``'/admin'`` endpoint.
        """
        return self._admin

    @property
    def db(self):
        """:class:`~driver.DataBase`: put or search doc from glitter.
        """
        return self._db


class NamespacedDriver:
    """Base class for creating endpoints (namespaced objects) that can be added
    under the :class:`~driver.GlitterClient` driver.
    """

    PATH = '/'

    def __init__(self, driver):
        """Initializes an instance of
        :class:`~GlitterClient_driver.driver.NamespacedDriver` with the given
        driver instance.

        Args:
            driver (GlitterClient): Instance of
                :class:`~GlitterClient_driver.driver.GlitterClient`.
        """
        self.driver = driver

    @property
    def transport(self):
        return self.driver.transport

    @property
    def api_prefix(self):
        return self.driver.api_prefix

    @property
    def path(self):
        return self.api_prefix + self.PATH


class DataBase(NamespacedDriver):
    """Exposes the data of glitter db.
    """

    def create_schema(self, schema_name, fields):
        """

        Args:
            - schema_name (str): the name of schema.
            - fields (:obj:`list` of :obj:`dic`): list of schema fields.

        Returns:
            - :obj:`dic`: request result.
        """
        path = '/create_schema'
        schema_type = "record"
        body = {
            "schema_name": schema_name,
            "data": {
                "type": schema_type,
                "name": schema_name,
                "fields": fields
            }
        }

        return self.transport.forward_request(
            method='POST',
            path=self.api_prefix + path,
            json=body,
        )

    def list_schema(self):
        """

        Returns:
            - :obj:`dic`: list all schema.
        """
        path = '/list_schema'

        return self.transport.forward_request(
            method='GET',
            path=self.api_prefix + path,
        )

    def show_schema(self, schema_name):
        """

        Args:
            - schema_name(str): the name of schema.
        Returns:
            - :obj:`dic`: result with document schema.
        """
        path = '/show_schema'

        return self.transport.forward_request(
            method='GET',
            path=self.api_prefix + path,
            params={"schema_name": schema_name}
        )

    def app_status(self):
        """

        Returns:
            - :obj:`dic`: result with document count.
        """

        path = '/app_status'

        return self.transport.forward_request(
            method='GET',
            path=self.api_prefix + path,
        )

    def put_doc(self, schema_name, doc_value):
        """Put document to glitter.

        Args:
            - schema_name(str): the name of schema.
            - doc_value(:obj:`dic`): doc content.

        Returns:
            - :obj:`dic`: result with code,msg,tx.
        """
        path = '/put_doc'
        body = {
            "schema_name": schema_name,
            "doc_data": doc_value,
        }
        return self.transport.forward_request(
            method='POST',
            path=self.api_prefix + path,
            json=body,
        )

    def get_docs(self, schema_name, primary_key):
        """Get documents from glitter by doc ids.

        Args:
            schema_name(str): the name of schema.
            primary_key(list of str): main key of document,must be uniq.

        Returns:
            :obj:`dic`: result with the document struct.
        """
        path = '/get_docs'
        return self.transport.forward_request(
            method='POST',
            path=self.api_prefix + path,
            json={"schema_name": schema_name, "doc_ids": primary_key},
        )

    def search(self, index, query_word, query_field, filters=[], aggs_field=[], order_by="", limit=10, page=1):
        """ search from glitter,with more args.

        Args:
            index(str): index name.
            query_word(str): query word, only applies to  query_field.
            query_field(:obj: `list` of str): query field must be indexed in schema.
            filters(:obj:`list` of :obj:`dic`): filter condition.
            aggs_field(:obj: `list` of str): aggregate field ,which is define in schema
            order_by(str): order field
            limit(int): limit
            page(int): page number,begin from 1

        Returns:
            :obj:`dic`: the documents match query words.
        """

        path = '/search'
        return self.transport.forward_request(
            method='POST',
            path=self.api_prefix + path,
            json={"index": index, "query": query_word, "filters": filters, "query_field": query_field,
                  "aggs_field": aggs_field, "order_by": order_by, "limit": limit, "page": page},
        )


class Chain(NamespacedDriver):
    PATH = '/chain/'

    def status(self):
        """ Get Tendermint status including node info, pubkey, latest block hash, app hash, block height, current max peer height, and time.

        Returns:
            :obj:`json`:Details of the HTTP API provided by the tendermint server.
        """
        path = "/chain/status"
        return self.transport.forward_request(
            method='GET',
            path=self.api_prefix + path,
        )

    def tx_search(self, query, page=1, per_page=30, order_by="desc", prove=True):
        """ Search for transactions their results

        Args:
            query(str): query words. (e.g: ``tx.height=1000, tx.hash='xxx', update_doc.token='test_token'``)
            page(int): page number. Defaults to ``1``.
            per_page(int): number of entries per page (max: ``100``).Defaults to ``30``.
            order_by(str): Order in which transactions are sorted (``asc`` or ``desc``), by height & index. If empty, default sorting will be still applied.
            prove(bool): Include proofs of the transactions inclusion in the block. Defaults to ``True``.

        Returns:
            :obj"`json`: transaction info
        """

        path = "/chain/tx_search"
        query = '"{}"'.format(query)
        order_by = '"{}"'.format(order_by)
        prove = "true" if prove else "false"

        return self.transport.forward_request(
            method='GET',
            path=self.api_prefix + path,
            params={'query': query, 'page': page, 'per_page': per_page, 'order_by': order_by, 'prove': prove},
        )

    def block_search(self, query, page=1, per_page=30, order_by="desc"):
        """Search for blocks by BeginBlock and EndBlock events

        Args:
            query(str): query condition. (e.g: ``block.height > 1000 AND valset.changed > 0``)
            page(int): page number
            per_page(int): number of entries per page (max: 100)
            order_by(str): order in which blocks are sorted ("asc" or "desc"), by height. If empty, default sorting will be still applied.
        Returns:
            :obj:`json`: block info

        """
        path = "/chain/block_search"
        query = '"{}"'.format(query)
        order_by = '"{}"'.format(order_by)

        return self.transport.forward_request(
            method='GET',
            path=self.api_prefix + path,
            params={'query': query, 'page': page, 'per_page': per_page, 'order_by': order_by},
        )

    def block(self, height=None):
        """ Get block at a specified height

        Args:
            height(int): height

        Returns:
            :obj:`json`:height to return. If no height is provided, it will fetch the latest block.

        """
        path = "/chain/block"
        params = {}
        if height is not None:
            params["height"] = height
        return self.transport.forward_request(
            method='GET',
            path=self.api_prefix + path,
            params=params,
        )

    def health(self):
        """ Get node health.

        Returns:
            Details of the HTTP API provided by the tendermint server, empty result (200 OK) on success, no response - in case of an error.
        """
        path = "/chain/health"
        return self.transport.forward_request(
            method='GET',
            path=self.api_prefix + path,
        )

    def net_info(self):
        """ Get network info.

        Returns:
            Details of the HTTP API provided by the tendermint server.

        """
        path = "/chain/net_info"
        return self.transport.forward_request(
            method='GET',
            path=self.api_prefix + path,
        )

    def blockchain(self, min_height=1, max_height=20):
        """ Get block headers for minHeight <= height maxHeight.
        If maxHeight does not yet exist, blocks up to the current height will be returned. If minHeight does not exist (due to pruning), earliest existing height will be used.
        At most 20 items will be returned. Block headers are returned in descending order (highest first).

        Args:
            min_height(int): Minimum block height to return
            max_height(bool): Maximum block height to return

        Returns:
            Block headers, returned in descending order (highest first).
        """

        path = "/chain/blockchain"
        return self.transport.forward_request(
            method='GET',
            path=self.api_prefix + path,
            params={"minHeight": min_height, "maxHeight": max_height}
        )

    def header(self, height=1):
        """ Retrieve the block header corresponding to a specified height.

        Args:
            height(int): height to return. If no height is provided, it will fetch the latest height.

        Returns:
            Header information.

        """
        path = "/chain/header"
        return self.transport.forward_request(
            method='GET',
            path=self.api_prefix + path,
            params={"height": height},
        )

    def header_by_hash(self, header_hash):
        """ Retrieve the block header corresponding to a block hash.

        Args:
            header_hash(str): header hash
        Returns:
        """
        path = "/chain/header_by_hash"
        return self.transport.forward_request(
            method='GET',
            path=self.api_prefix + path,
            params={"hash": header_hash},
        )

    def block_by_hash(self, *, header_hash):
        """ Get block by hash

        Args:
            header_hash(str): block hash. example: "0xD70952032620CC4E2737EB8AC379806359D8E0B17B0488F627997A0B043ABDED"

        Returns:

        """
        path = "/chain/header_by_hash"
        return self.transport.forward_request(
            method='GET',
            path=self.api_prefix + path,
            params={"hash": header_hash},
        )


class Admin(NamespacedDriver):
    """Exposes functionality of the ``'/admin'`` endpoint.
    """

    def update_validator(self, pub_key, power=0, headers=None):
        """ update validator set

        Args:
            pub_key (str): public key
            power (int): power
            headers (dict): http header

        Returns:
            :obj:`dic`:

        """
        path = "/admin/update_validator"
        return self.transport.forward_request(
            method='POST',
            path=self.api_prefix + path,
            params={'pub_key': pub_key, 'power': power},
            headers=headers
        )

    def validators(self, height=None, page=1, per_page=100):
        """ Get validator set at a specified height

        Args:
            height (str): height to return. If no height is provided, it will fetch validator set which corresponds to the latest block.
            page (int): Page number (1-based)
            per_page (int): Number of entries per page (max: 100)

        Returns:
            :obj:`json`: Validators. Validators are sorted first by voting power (descending), then by address (ascending).

        """
        path = "/chain/validators"
        params = {"page": page, "per_page": per_page}
        if height is not None:
            params["height"] = height

        return self.transport.forward_request(
            method='GET',
            path=self.api_prefix + path,
            params=params,
        )
