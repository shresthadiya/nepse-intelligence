import api from "./client";

export const getNews = async ({
                                  companyId,
                                  source,
                                  skip = 0,
                                  limit = 20,
                              } = {}) => {
    const response = await api.get("/api/news/", {
        params: {
            company_id: companyId,
            source,
            skip,
            limit,
        },
    });

    return response.data;
};

export const recategorizeNews = async (
    newsId,
    categoryId
) => {
    const response = await api.post(
        `/api/news/${newsId}/recategorize`,
        null,
        {
            params: {
                category_id: categoryId,
            },
        }
    );

    return response.data;
};