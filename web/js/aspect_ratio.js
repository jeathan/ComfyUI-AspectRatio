import { app } from "../../../scripts/app.js";

// 在节点上直接显示判断出的图片比例（如 "16:9"），并把预览框压缩到单行高度。

app.registerExtension({
	name: "ImageAspectRatio.Display",
	async beforeRegisterNodeDef(nodeType, nodeData, app) {
		if (nodeData.name !== "ImageAspectRatio") return;

		const api = () => window.comfyAPI?.textPreviewWidgets;

		function shrinkPreview(node) {
			const preview = node.widgets?.find((w) => w.name === "preview_text");
			if (!preview) return;

			// 让节点预留空间按 22px 计算
			if (preview.options) {
				preview.options.getMinHeight = () => 22;
				preview.options.getMaxHeight = () => 22;
			}
			preview.computeLayoutSize = () => ({ minHeight: 22, maxHeight: 22, minWidth: 0 });

			// 直接把渲染出来的 DOM 高度压成单行
			requestAnimationFrame(() => {
				const el = preview.element?.querySelector?.(".widget-text-preview") ?? preview.element;
				if (el) {
					el.style.minHeight = "22px";
					el.style.maxHeight = "22px";
					el.style.height = "22px";
					el.style.overflow = "hidden";
				}
				node.setSize?.(node.computeSize?.());
				app.graph?.setDirtyCanvas?.(true, false);
			});
		}

		const onNodeCreated = nodeType.prototype.onNodeCreated;
		nodeType.prototype.onNodeCreated = function () {
			onNodeCreated?.apply(this, arguments);
			api()?.addTextPreviewWidgets?.(this);

			// 隐藏 Markdown/Plain text 切换开关
			const mode = this.widgets?.find((w) => w.name === "preview_mode");
			if (mode?.options) mode.options.hidden = true;

			shrinkPreview(this);
		};

		const onExecuted = nodeType.prototype.onExecuted;
		nodeType.prototype.onExecuted = function (message) {
			onExecuted?.apply(this, arguments);
			api()?.updateTextPreviewWidgets?.(this, message);
			shrinkPreview(this);
		};
	},
});
