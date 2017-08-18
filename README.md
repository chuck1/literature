
## Data

 * mongodb
   * tables
     * articles
     * authors

## Interface

 * mongodb shell
 * python script that takes a filter and generates a grpahviz plot of article connections

Inserting an article

    >>> a=[author_id(s) for s in ['michel x goemans','neil olver','thomas rothvob','rico zenklusen']]
    >>> db.articles.insert({'title':'matroids and integrality gaps for hypergraphic steiner tree relaxations','authors':a})

Generating the plot

    python3 -i plot.py
    >>> plot({})

