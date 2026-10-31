import api from "./client";

export const getCompanies = async () => {
    const response = await api.get("/api/companies");
    return response.data;
};

export const getCompanyPrices = async (
    companyId,
    range = "30d"
) => {
    const response = await api.get(
        `/api/companies/${companyId}/prices`,
        { params: { range } }
    );

    return response.data;
};

export const getCompanyBehavior = async (companyId) => {
    const response = await api.get(
        `/api/companies/${companyId}/behavior-summary`
    );

    return response.data;
};