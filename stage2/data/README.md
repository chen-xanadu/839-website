## Web Data Sources

We extracted movie information from:
- **IMDb** (**Internet Movie Database**): [https://www.imdb.com/](https://www.imdb.com/)
- **Metacritic**: [https://www.metacritic.com/](https://www.metacritic.com/)

## Entity Type
Our entity type is **movie information**. 

##  Table Description

### Table Size

| | IMDb  | Metacritic |
| --- | :---: | :---: |
| **Number of tuples** | 3094  | 3345  |

### Table Schema

| Attribute | Description |
| --- | --- |
| id | The index assigned to each movie, starting from 1 for each table |
| title | The name of the movie |
| release year | The year in which the movie was released |
| rating | The rating of the movie (e.g. PG-13, R) |
| runtime | The length of the movie |
| genres | The genres of the movie, separated by commas |
| director | The directors of the movie, separated by commas |
| starring | The main cast of the movie, separated by commas |
| countries | The places where the production companies for the movie are based in, separated by commas |
| languages | The languages that are spoken in the movie, separated by commas |
| production company | The companies that produced the movie, separated by commas |
| writers | The writers of the movie, as appeared in the credit, separated by commas |
| score | The user/media score for the movie |

