const MUNIS = [
    { muni: "sr", name: "Städteregion Aachen" },
    { muni: "aachen", name: "Aachen" },
    { muni: "alsdorf", name: "Alsdorf" },
    { muni: "baesweiler", name: "Baesweiler" },
    { muni: "eschweiler", name: "Eschweiler" },
    { muni: "herzogenrath", name: "Herzogenrath" },
    { muni: "monschau", name: "Monschau" },
    { muni: "roetgen", name: "Roetgen" },
    { muni: "simmerath", name: "Simmerath" },
    { muni: "stolberg", name: "Stolberg" },
    { muni: "wuerselen", name: "Würselen" }
]
export const MUNI_DICT = {
    "sr": "die Städteregion Aachen",
    "aachen": "Aachen",
    "alsdorf": "Alsdorf",
    "baesweiler": "Baesweiler",
    "eschweiler": "Eschweiler",
    "herzogenrath": "Herzogenrath",
    "monschau": "Monschau",
    "roetgen": "Roetgen",
    "simmerath": "Simmerath",
    "stolberg": "Stolberg",
    "wuerselen": "Würselen"
}

export function genMetaInfo(title, description) {
    return {
        title: title,
        meta: [
            { name: "description", content: description },
            { name: "twitter:description", content: description },
            { name: "og:description", content: description },
            { name: "twitter:title", content: title },
            { name: "og:title", content: title },
        ]
    }
}
