import api from "./client";

export const triggerCrawl = async () => {
    const response = await api.post("/api/admin/crawl-runs");
    return response.data;
};

export const getHealth = async () => {
    const response = await api.get("/health");
    return response.data;
};