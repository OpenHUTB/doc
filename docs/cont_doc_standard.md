# 文档标准

本文档将作为为文档做出贡献而需要遵循的一些规则的指南和示例。


*   [__文档结构__](#docs_structure)  
*   [__规则__](#rules)  
*   [__全局变量__](#variables)  
*   [__例外情况__](#exceptions)  

---
## 文档结构 <span id="docs_structure"></span>

我们和 [`extra.css`](https://github.com/carla-simulator/carla/tree/master/Docs/extra.css) 一起，混合使用 Markdown 和 HTML 标签来自定义文档和文件。要更新 Python API 文档，您需要编辑  [`carla/PythonAPI/docs/`][fileslink] 内部相应的 YAML 文件并运行 [`doc_gen.py`][scriptlink] 或 `make PythonAPI.docs`，而不是直接修改 Markdown。

这将在 `carla/Docs/` 中重新生成相应的 Markdown 文件，然后可以将其输入到 `mkdocs`.

[fileslink]: https://github.com/carla-simulator/carla/tree/master/PythonAPI/docs
[scriptlink]: https://github.com/carla-simulator/carla/blob/master/PythonAPI/docs/doc_gen.py

---
## 规则 <span id="rules"></span>

*   各节之间和文档末尾始终留有空行。
*   除 HTML 相关内容、Markdown 表格、代码片段和引用链接外，书写不应超过 `100` 列。
*   如果内联链接超出限制，请使用引用的 `[name][reference_link]` markdown 符号`[reference_link]: https://`，而不是`[name](https://)`。 
*   使用 `<br>` 进行内联跳转，而不是在行尾留下两个空格。
*   在新页面的开头使用 `<h1>Title</h1>` ，以制作标题或 `<hx>Heading<hx>` 制作**不会显示**在导航栏上的标题。
*   使用 `------` 强调标题或 `#` 层次结构下划线来制作标题并将其显示在导航栏中。

---
## 全局变量 <span id="variables"></span>

同一个链接或文案需要在多个页面出现时，不要逐页复制，统一在 `mkdocs.yml` 的
`extra.variables` 中定义，页面里用 `{{ 变量名 }}` 引用：

```yaml
extra:
  variables:
    wx_gzh_url: 'https://mp.weixin.qq.com/s/Fxfh98b-UEpJhbINDjroJQ'
```

```markdown
[公众号]({{ wx_gzh_url }})
```

`hooks.py` 在渲染页面之前完成替换；上例的 `[公众号](...)` 最终会指向配置中的地址。

*   变量名只能包含字母、数字和下划线。
*   未定义的变量保持原样，不会导致构建失败。
*   围栏代码块（三个反引号或 `~~~` 包围的内容）中的文本不会被替换。

---
## 例外情况 <span id="exceptions"></span>

  * 通过 Python 脚本生成的文档，例如 PythonAPI 参考

方便的 markdown [cheatsheet][cheatlink]。

[cheatlink]: https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet
