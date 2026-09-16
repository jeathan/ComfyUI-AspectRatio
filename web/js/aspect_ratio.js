import { app } from "../../../scripts/app.js";

// 在节点上直接显示判断出的图片比例（如 "16:9"），并把预览框压缩到单行高度。
// 关键：textPreview 用的是 <textarea>（Tailwind min-h-16 = 64px）或 markdown div（min-h-[60px]），
// 所以需要覆盖这两个内部元素的高度，而不只是外层容器。

app.registerExtension({
	name: "ImageAspectRatio.Display",
	async beforeRegisterNodeDef(nodeType, nodeData, app) {
		if (nodeData.name !== "ImageAspectRatio") return;

		const api = () => window.comfyAPI?.textPreviewWidgets;

		// 注入 CSS，把文本预览内容压成单行（!important 覆盖 Tailwind 的 min-h-16 / min-h-[60px]）
		const styleId = "iar-aspect-ratio-preview";
		if (!document.getElementById(styleId)) {
			const style = document.createElement("style");
			style.id = styleId;
			style.textContent = [
				".widget-text-preview textarea,",
				".widget-text-preview .comfy-markdown-content {",
				"  min-height: 22px !important;",
				"  max-height: 22px !important;",
				"  height: 22px !important;",
				"  padding-top: 2px !important;",
				"  padding-bottom: 2px !important;",
				"  overflow: hidden !important;",
				"}",
			].join("\n");
			document.head.appendChild(style);
		}

		function shrinkPreview(node) {
			const preview = node.widgets?.find((w) => w.name === "preview_text");
			if (!preview) return;
			if (preview.options) {
				preview.options.getMinHeight = () => 22;
				preview.options.getMaxHeight = () => 22;
			}
			preview.computeLayoutSize = () => ({ minHeight: 22, maxHeight: 22, minWidth: 0 });
			requestAnimationFrame(() => {
				node.setSize?.(node.computeSize?.());
				app.graph?.setDirtyCanvas?.(true, false);
			});
		}

		function removePreviewMode(node) {
			if (!node.widgets) return;
			const idx = node.widgets.findIndex((w) => w.name === "preview_mode");
			if (idx < 0) return;
			const w = node.widgets[idx];
			try { w.onRemove?.(); } catch (e) {}
			node.widgets.splice(idx, 1);
			if (w.element) w.element.style.display = "none";
		}

		const onNodeCreated = nodeType.prototype.onNodeCreated;
		nodeType.prototype.onNodeCreated = function () {
			onNodeCreated?.apply(this, arguments);
			api()?.addTextPreviewWidgets?.(this);
			removePreviewMode(this);
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
