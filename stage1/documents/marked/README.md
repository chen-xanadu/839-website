In this stage, the entity we tried to extract from the texts is "person name".
We put `<p>` ahead of the person name and `</p>` after it. So the marked person name should look like `<p>....</p>`.

If a name contains multiple words, we marked them separately.

```
Ex. 1
(In Raw text)
Now that Chris Chen and his father

(In Marked text)
Now that <p>Chris</p> <p>Chen</p> and his father
```

If a name has a possessive suffix (`'s`), we exclude the suffix from the tag.

```
Ex. 2
(In Raw text)
Now that Davy Jones's girlfriend, Rose, have reached....

(In Marked text)
Now that <p>Davy</p> <p>Jones</p>'s girlfriend, <p>Rose</p> , have reached ....
```
