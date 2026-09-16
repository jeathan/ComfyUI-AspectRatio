import { app } from "../../../scripts/app.js";
import { ComfyWidgets } from "../../../scripts/widgets.js";

// 在节点上直接显示判断出的图片比例（如 "16:9"）。
// 原理：节点后端通过 {"ui": {"text": [...]}} 返回比例文本，
// 这里在 onExecuted 时把它渲染成一个只读的文本显示控件。

app.registerExtension({
	name: "ImageAspectRatio.Display",
	async beforeRegisterNodeDef(nodeType, nodeData, app) {
		if (nodeData.name !== "ImageAspectRatio") return;

		function populate(text) {
			// 先移除上一次执行产生的显示控件（本节点的 image 输入是 socket，没有转换 widget）
			if (this.widgets) {
				const isConvertedWidget = +!!this.inputs?.[0]?.widget;
				for (let i = isConvertedWidget; i < this.widgets.length; i++) {
					this.widgets[i].onRemove?.();
				}
				this.widgets.length = isConvertedWidget;
			}

			const v = Array.isArray(text) ? text : [text];
			for (let line of v) {
				if (Array.isArray(line)) line = line[0];
				const w = ComfyWidgets["STRING"](this, "ratio", ["STRING", { multiline: false }], app).widget;
				w.inputEl.readOnly = true;
				w.inputEl.style.opacity = 0.6;
				w.value = line;
			}

			requestAnimationFrame(() => {
				const sz = this.computeSize();
				if (sz[0] < this.size[0]) {
					sz[0] = this.size[0];
				}
				if (sz[1] < this.size[1]) {
					sz[1] = this.size[1];
				}
				this.onResize?.(sz);
				app.graph.setDirtyCanvas(true, false);
			});
		}

		const onExecuted = nodeType.prototype.onExecuted;
		nodeType.prototype.onExecuted = function (message) {
			onExecuted?.apply(this, arguments);
			if (message && message.text) {
				populate.call(this, message.text);
			}
		};
	},
});
