## ninuXoo JSON API

### Search Operations
| **Operation** |  **Description** | **URL** | ***NOTES*** |
| :--- | :--- | :--- | :--- |
| `exactquery` | Return the search results that match exactly (i.e. performing an AND between the exact words) `querystring`.<br />The optional parameter `ip` restricts the search to a given server IP address.<br />The optional parameter `filetype` restricts the search to a given filetype/extension. | /json.cgi?op=**exactquery**&q=`querystring`&ip=`IP address`&filetype=`extension` ||
| `orquery` | Return the search results that match the single exact words in *querystring*.<br />The optional parameter `ip` restricts the search to a given server IP address.<br />The optional parameter `filetype` restricts the search to a given filetype/extension. | /json.cgi?op=**orquery**&q=`querystring`&ip=`IP address`&filetype=`extension` ||
| `likequery` | Return search results by performing variations on the words in `querystring`, limiting to no more than `word limit` words.<br />The optional parameter `ip` restricts the search to a given server IP address.<br />The optional parameter `filetype` restricts the search to a given filetype/extension. | /json.cgi?op=**likequery**&q=`querystring`&words=`word limit`&ip=`IP address`&filetype=`extension` ||
| `query` | Return search results by applying in order the exactquery, orquery and likequery operations, trying to retrieve at least `nresults` results.<br />The optional parameter `ip` restricts the search to a given server IP address.<br />The optional parameter `filetype` restricts the search to a given filetype/extension. | /json.cgi?op=**query**&q=`querystring`&nresults=`nresults`&ip=`IP address`&filetype=`extension` | Default value of `nresults` is `200` |
| `whatsnew` | Return the resources that have been recently discovered, trying to retrieve at least <nresults> results, but no more than `nresults` | /json.cgi?op=**whatsnew**&nresults=`nresults` | Default value for `nresults` is `200` |
| `serverlist` | Return the list of found servers | /json.cgi?op=**serverlist** ||

#### Other Operations
| **Operation** |  **Description** | **URL** |
| :--- | :--- | :--- | :--- |
| `resourcestats` | Return the total number of resources currently indexed by the Search Engine | /json.cgi?op=**resourcestats** |
| `serverstats` | Return the total number of servers currently indexed by the Search Engine | /json.cgi?op=**serverstats** |

#### Other Operations (Response/Result Format)
| **Operation** |  **Description** |
| :--- | :--- |
| `responsen` | Response number |
| `response` | Response description |
| `result` | Result |

***

### Search Results Format
| **Operation** | **Values** *or* **Description** |
| :--- | :--- |
| `response number` |  `200` = *OK*<br />`400` = *Bad request*<br />`418` = *I'm a teapot*<br />`500` = *Server error*<br />`501` = *Not implemented* |
| `response description` | *Textual description of the response* |
| `number of result labels` | *Number of set of results found* |
| `search time` | *Time, in seconds, needed to perform the search* |
| `results label` | *The search term or terms that yield to the following results* |
| `exact result flag` | `true` = *`exact` result*<br />`false` = *`or` or `like` result* |
| `number of results` | *Number of resources in the `resources` object* |
| `label` | *The (partial) path on the server* |
| `hierarchy rank` | *The level of the trie's hierarchy.*<br />`2` = *Server's IP/hostname*<br />`1` = *Other protocols (e.g. "smb:")* |
| `resource URI` | *The resource's complete URI* |
| `file name` | *The resource's file name* |
| `file type` | *The resource's file type* |

#### Example
```jsonp
{
    responsen: <response number>,
    response: <response description>,
    q: <search terms>,
    nresults: <number of results>,
	nlabels: <number of result labels>,
	searchtime: <search time>,
    results: [
               {
               resultlabel: <results label>,
               exactresult: <exact result flag>,
               nresults: <number of results>,
               resourcetrie: {
                           label: <label>,
                           rank: <hierarchy rank>,
                           resources: [
                                {
                                    uri: <resource URI>,
                                    filename: <file name>,
                                    filetype: <file type>
                                },
                                {
                                    uri: <resource URI>,
                                    filename: <file name>,
                                    filetype: <file type>
                                },
                                ...
                           ],
                           children: [
                                {
                                    label: <label>,
                                    rank: <hierarchy rank>,
                                    resources [
                                       ...
                                    ],
                                    children: [
                                       ...
                                    ]
                                },
                                {
                                    label: <label>,
                                    rank: <hierarchy rank>,
                                    resources {
                                       ...
                                    },
                                    children: {
                                       ...
                                    }
                                },
                                ...
                           ]
               }
         },
         {
               resultlabel: <results label>,
               exactresult: <exact result flag>,
               nresults: <number of results>,
               resourcetrie: {
                      ...
               }
         },
         ...
    ]
}
```

