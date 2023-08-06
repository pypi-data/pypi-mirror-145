# Templatizer
Templatizer allows for sprinkling in some imperative logic to your declarative configuration files.

## Why Imperative?
While a fully declarative configuration file is often nice to be able to describe the _intended_ state of the world in a single place, these can also become _quite_ verbose over time.

For Kubernetes, for example, you might be configuring a number of monitoring jobs. These will have different storage, CPU, and memory requirements. They also have unique configuration requirements for each one. I might be holding it wrong, but I find this very hard to make work in Helm and Kustomize without repeating myself over and over again.

What I want is something that runs _before_ Helm, Kustomize, and whatever other tools you're using. I want something to generate files with the ability to do imperative logic first.

## Example
```python
import templatizer

class Simple(templatizer.Templatable):
    prop = 12345

class Imperative(templatizer.Templatable):
    tick = 0

    def prop(self):
        return 12345 + self.tick

simple = Simple()
assert simple.propval('prop') == 12345

imperative = Imperative()
assert imperative.propval('prop') == 12345
imperative.tick = 1
assert imperative.propval('prop') == 12346
```

The `templatizer.run` function takes a list of `Templatable` objects, generates them into strings, and adds separators in between. By default the `---` separator is used, which is useful for generating YAML documents. This can be changed to suit your use case.

## Kubernetes
The `templatizer.k8s` module includes generated definitions from the [Kubernetes OpenAPI Spec](https://github.com/kubernetes/kubernetes/blob/master/api/openapi-spec/swagger.json).

This allows for generating Kubernetes manifests with imperative hooks. Examples of this are provided in the `examples/` directory.