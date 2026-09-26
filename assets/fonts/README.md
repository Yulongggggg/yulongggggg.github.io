# Chinese name font

The homepage renders 刘雨龙 as selectable text using a self-hosted, three-character
subset of LXGW WenKai Regular. The subset is named Yulong Name Kai to distinguish
it from the original font. No generated lettering image is used.

- Upstream: https://github.com/lxgw/LxgwWenKai
- Source commit: 8bd6319350fb3ae1904c1cb1a41595ab15d21140
- Source font: https://raw.githubusercontent.com/lxgw/LxgwWenKai/8bd6319350fb3ae1904c1cb1a41595ab15d21140/fonts/TTF/LXGWWenKai-Regular.ttf
- License: SIL Open Font License 1.1, reproduced in OFL.txt.
- Subset characters: U+5218, U+96E8, U+9F99.
- Process: fontTools subset, preserve all name/license records, rename the subset family,
  and encode as WOFF. No glyph outlines were altered.
