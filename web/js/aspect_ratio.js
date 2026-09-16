import { app } from "../../../scripts/app.js";

// 在节点上直接显示判断出的图片比例（如 "16:9"）。
// 新版前端用 TEXT_PREVIEW 控件显示 ui.text（与内置 PreviewAny / SaveText 完全一致），
// 因此直接调用前端暴露的 textPreviewWidgets API。

app.registerExtension({
	name: "ImageAspectRatio.Display",
	async beforeRegisterNodeDef(nodeType, nodeData, app) {
		if (nodeData.name !== "ImageAspectRatio") return;

		const api = () => window.comfyAPI?.textPreviewWidgets;

		const onNodeCreated = nodeType.prototype.onNodeCreated;
		nodeType.prototype.onNodeCreated = function () {
			onNodeCreated?.apply(this, arguments);
			api()?.addTextPreviewWidgets?.(this);
		};

		const onExecuted = nodeType.prototype.onExecuted;
		nodeType.prototype.onExecuted = function (message) {
			onExecuted?.apply(this, arguments);
			api()?.updateTextPreviewWidgets?.(this, message);
		};
	},
});
