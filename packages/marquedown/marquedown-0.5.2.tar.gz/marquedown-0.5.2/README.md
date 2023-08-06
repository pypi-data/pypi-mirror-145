# Marquedown

Extending Markdown further by adding a few more useful notations.
It can be used in place of `markdown` as it also uses and applies it.

## Examples

### Blockquote with citation

This is currently limited to the top scope with no indentation.
Surrounding dotted lines are optional.

```md
......................................................
> You have enemies? Good. That means you've stood up
> for something, sometime in your life.
-- Winston Churchill
''''''''''''''''''''''''''''''''''''''''''''''''''''''
```

```html
<blockquote>
    <p>
        You have enemies? Good. That means you've stood up
        for something, sometime in your life.
    </p>
    <cite>Winston Churchill</cite>
</blockquote>
```

### Embed video

#### YouTube

```md
![dimweb](https://youtu.be/VmAEkV5AYSQ "An embedded YouTube video")
```

```html
<iframe
    src="https://www.youtube.com/embed/VmAEkV5AYSQ"
    title="An embedded YouTube video" frameborder="0"
    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
    allowfullscreen>
</iframe>
```

## Commands

### `render`: Render documents

You can render an entire directory and its subdirectories of Markdown or Marquedown documents. This can be used to automate rendering pages for your website.

Do `python -m marquedown render --help` for list of options.

#### Example

For a few of my websites hosted on GitLab, I have it set up to run *this* on push:

```sh
# Render document
python -m marquedown render -i ./md -o ./public -t ./templates/page.html

# This is for the GitLab Pages publication
mkdir .public
cp -r public .public
mv .public public  
```