import api from "./api";

class SummaryService {
  basicSummary() {
    return api.get("/transactions-service/summary").then((response) => {
      return response.data;
    });
  }
}

export default new SummaryService();
