Ошиибки и предупреждения:
open-webui\src\components\DiagramEditor\DiagramEditor.tsx
[{
	"resource": "/e:/Сode/C4Designer/open-webui/src/App.tsx",
	"owner": "typescript",
	"code": "2307",
	"severity": 8,
	"message": "Не удается найти модуль \"./components/DiagramEditor/DiagramEditor\" или связанные с ним объявления типов.",
	"source": "ts",
	"startLineNumber": 2,
	"startColumn": 27,
	"endLineNumber": 2,
	"endColumn": 69
},{
	"resource": "/e:/Сode/C4Designer/open-webui/src/App.tsx",
	"owner": "typescript",
	"code": "2307",
	"severity": 8,
	"message": "Не удается найти модуль \"./components/InputPanel/InputPanel\" или связанные с ним объявления типов.",
	"source": "ts",
	"startLineNumber": 3,
	"startColumn": 24,
	"endLineNumber": 3,
	"endColumn": 60
},{
	"resource": "/e:/Сode/C4Designer/open-webui/src/App.tsx",
	"owner": "typescript",
	"code": "2307",
	"severity": 8,
	"message": "Не удается найти модуль \"./components/CodePanel/CodePanel\" или связанные с ним объявления типов.",
	"source": "ts",
	"startLineNumber": 4,
	"startColumn": 23,
	"endLineNumber": 4,
	"endColumn": 57
},{
	"resource": "/e:/Сode/C4Designer/open-webui/src/App.tsx",
	"owner": "typescript",
	"code": "2307",
	"severity": 8,
	"message": "Не удается найти модуль \"./components/AIAssistant/AIAssistant\" или связанные с ним объявления типов.",
	"source": "ts",
	"startLineNumber": 5,
	"startColumn": 25,
	"endLineNumber": 5,
	"endColumn": 63
},{
	"resource": "/e:/Сode/C4Designer/open-webui/src/App.tsx",
	"owner": "typescript",
	"code": "2769",
	"severity": 8,
	"message": "Ни одна перегрузка не соответствует этому вызову.\n  Перегрузка 1 из 2, \"(props: { component: ElementType<any, keyof IntrinsicElements>; } & GridBaseProps & { sx?: SxProps<Theme> | undefined; } & SystemProps<...> & Omit<...>): Element | null\", возвратила следующую ошибку.\n    Свойство \"component\" отсутствует в типе \"{ children: Element; item: true; xs: number; sx: { height: string; }; }\" и является обязательным в типе \"{ component: ElementType<any, keyof IntrinsicElements>; }\".\n  Перегрузка 2 из 2, \"(props: DefaultComponentProps<GridTypeMap<{}, \"div\">>): Element | null\", возвратила следующую ошибку.\n    Тип \"{ children: Element; item: true; xs: number; sx: { height: string; }; }\" не может быть назначен для типа \"IntrinsicAttributes & GridBaseProps & { sx?: SxProps<Theme> | undefined; } & SystemProps<Theme> & Omit<...>\".\n      Свойство \"item\" не существует в типе \"IntrinsicAttributes & GridBaseProps & { sx?: SxProps<Theme> | undefined; } & SystemProps<Theme> & Omit<...>\".",
	"source": "ts",
	"startLineNumber": 54,
	"startColumn": 10,
	"endLineNumber": 54,
	"endColumn": 14,
	"relatedInformation": [
		{
			"startLineNumber": 64,
			"startColumn": 5,
			"endLineNumber": 64,
			"endColumn": 14,
			"message": "Здесь объявлен \"component\".",
			"resource": "/e:/Сode/C4Designer/open-webui/node_modules/@mui/types/esm/index.d.ts"
		}
	]
},{
	"resource": "/e:/Сode/C4Designer/open-webui/src/App.tsx",
	"owner": "typescript",
	"code": "2769",
	"severity": 8,
	"message": "Ни одна перегрузка не соответствует этому вызову.\n  Перегрузка 1 из 2, \"(props: { component: ElementType<any, keyof IntrinsicElements>; } & GridBaseProps & { sx?: SxProps<Theme> | undefined; } & SystemProps<...> & Omit<...>): Element | null\", возвратила следующую ошибку.\n    Свойство \"component\" отсутствует в типе \"{ children: Element[]; item: true; xs: number; sx: { display: \"flex\"; flexDirection: \"column\"; height: string; }; }\" и является обязательным в типе \"{ component: ElementType<any, keyof IntrinsicElements>; }\".\n  Перегрузка 2 из 2, \"(props: DefaultComponentProps<GridTypeMap<{}, \"div\">>): Element | null\", возвратила следующую ошибку.\n    Тип \"{ children: Element[]; item: true; xs: number; sx: { display: \"flex\"; flexDirection: \"column\"; height: string; }; }\" не может быть назначен для типа \"IntrinsicAttributes & GridBaseProps & { sx?: SxProps<Theme> | undefined; } & SystemProps<Theme> & Omit<...>\".\n      Свойство \"item\" не существует в типе \"IntrinsicAttributes & GridBaseProps & { sx?: SxProps<Theme> | undefined; } & SystemProps<Theme> & Omit<...>\".",
	"source": "ts",
	"startLineNumber": 60,
	"startColumn": 10,
	"endLineNumber": 60,
	"endColumn": 14,
	"relatedInformation": [
		{
			"startLineNumber": 64,
			"startColumn": 5,
			"endLineNumber": 64,
			"endColumn": 14,
			"message": "Здесь объявлен \"component\".",
			"resource": "/e:/Сode/C4Designer/open-webui/node_modules/@mui/types/esm/index.d.ts"
		}
	]
},{
	"resource": "/e:/Сode/C4Designer/open-webui/src/App.tsx",
	"owner": "typescript",
	"code": "6133",
	"severity": 4,
	"message": "Свойство \"requirements\" объявлено, но его значение не было прочитано.",
	"source": "ts",
	"startLineNumber": 14,
	"startColumn": 32,
	"endLineNumber": 14,
	"endColumn": 44,
	"tags": [
		1
	]
}]



src\components\DiagramEditor\CustomNode.tsx
[{
	"resource": "/e:/Сode/C4Designer/open-webui/src/components/DiagramEditor/CustomNode.tsx",
	"owner": "typescript",
	"code": "1484",
	"severity": 8,
	"message": "' NodeProps ' является типом и должен быть импортирован с использованием импорта только типа, если включен 'verbatimModuleSyntax'.",
	"source": "ts",
	"startLineNumber": 2,
	"startColumn": 28,
	"endLineNumber": 2,
	"endColumn": 37
}]


src\components\DiagramEditor\DiagramEditor.tsx
[{
	"resource": "/e:/Сode/C4Designer/open-webui/src/components/DiagramEditor/DiagramEditor.tsx",
	"owner": "typescript",
	"code": "1484",
	"severity": 8,
	"message": "' Node ' является типом и должен быть импортирован с использованием импорта только типа, если включен 'verbatimModuleSyntax'.",
	"source": "ts",
	"startLineNumber": 6,
	"startColumn": 3,
	"endLineNumber": 6,
	"endColumn": 7
},{
	"resource": "/e:/Сode/C4Designer/open-webui/src/components/DiagramEditor/DiagramEditor.tsx",
	"owner": "typescript",
	"code": "1484",
	"severity": 8,
	"message": "' Edge ' является типом и должен быть импортирован с использованием импорта только типа, если включен 'verbatimModuleSyntax'.",
	"source": "ts",
	"startLineNumber": 7,
	"startColumn": 3,
	"endLineNumber": 7,
	"endColumn": 7
},{
	"resource": "/e:/Сode/C4Designer/open-webui/src/components/DiagramEditor/DiagramEditor.tsx",
	"owner": "typescript",
	"code": "1484",
	"severity": 8,
	"message": "' NodeTypes ' является типом и должен быть импортирован с использованием импорта только типа, если включен 'verbatimModuleSyntax'.",
	"source": "ts",
	"startLineNumber": 8,
	"startColumn": 3,
	"endLineNumber": 8,
	"endColumn": 12
},{
	"resource": "/e:/Сode/C4Designer/open-webui/src/components/DiagramEditor/DiagramEditor.tsx",
	"owner": "typescript",
	"code": "2307",
	"severity": 8,
	"message": "Не удается найти модуль \"./CustomNode\" или связанные с ним объявления типов.",
	"source": "ts",
	"startLineNumber": 14,
	"startColumn": 24,
	"endLineNumber": 14,
	"endColumn": 38
},{
	"resource": "/e:/Сode/C4Designer/open-webui/src/components/DiagramEditor/DiagramEditor.tsx",
	"owner": "typescript",
	"code": "6133",
	"severity": 4,
	"message": "Свойство \"Edge\" объявлено, но его значение не было прочитано.",
	"source": "ts",
	"startLineNumber": 7,
	"startColumn": 3,
	"endLineNumber": 7,
	"endColumn": 7,
	"tags": [
		1
	]
}]



NER-Модель (обучена), структура папки (backend/ner_model-20250625T131736Z-1-001/ner_model):
config.json
model.safetensors
special_tokens_map.json
tokenizer.json
tokenizer_config.json
vocab.txt

RE-Модель (обучена), структура папки (backend/re_model_v2-20250625T151402Z-1-001/re_model_v2l):
added_tokens.json
config.json
model.safetensors
special_tokens_map.json
tokenizer.json
tokenizer_config.json
vocab.txt