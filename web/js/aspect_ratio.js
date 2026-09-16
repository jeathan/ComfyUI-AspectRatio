import { app } from "../../../scripts/app.js";

// 在节点上直接显示判断出的图片比例（如 "16:9"），并把预览框缩到最小、只显示一行数值。

app.registerExtension({
	name: "ImageAspectRatio.Display",
	async beforeRegisterNodeDef(nodeType, nodeData, app) {
		if (nodeData.name !== "ImageAspectRatio") return;

		const api = () => window.comfyAPI?.textPreviewWidgets;

		const onNodeCreated = nodeType.prototype.onNodeCreated;
		nodeType.prototype.onNodeCreated = function () {
			onNodeCreated?.apply(this, arguments);
			api()?.addTextPreviewWidgets?.(this);

			// 把预览框最小高度压到单行，去掉多余空间
			const preview = this.widgets?.find((w) => w.name === "preview_text");
			if (preview?.options) {
				preview.options.getMinHeight = () => 22;
			}

			// 隐藏 Markdown/Plain text 切换开关，只保留数值
			const mode = this.widgets?.find((w) => w.name === "preview_mode");
			if (mode?.options) {
				mode.options.hidden = true;
			}

			requestAnimationFrame(() => {
				this.setSize?.(this.computeSize());
				app.graph?.setDirtyCanvas?.(true, false);
			});
		};

		const onExecuted = nodeType.prototype.onExecuted;
		nodeType.prototype.onExecuted = function (message) {
			onExecuted?.apply(this, arguments);
			api()?.updateTextPreviewWidgets?.(this, message);
		};
	},
});
