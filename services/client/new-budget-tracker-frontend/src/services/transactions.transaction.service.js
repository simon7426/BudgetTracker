import api from "./api";

class TransactionService {
  addTransaction({
    transaction_type,
    transaction_date,
    transaction_description,
    transaction_amount,
    transaction_category_id,
    transaction_account_id,
  }) {
    return api
      .post("/transactions-service/transactions", {
        transaction_type,
        transaction_date,
        transaction_description,
        transaction_amount,
        transaction_category_id,
        transaction_account_id,
      })
      .then((response) => {
        return response.data;
      });
  }

  getTransactions(keyset, limit) {
    return api
      .get("/transactions-service/transactions", { params: { keyset, limit } })
      .then((response) => {
        return response.data;
      });
  }

  editTransaction({
    transaction_id,
    transaction_date,
    transaction_type,
    transaction_description,
    transaction_amount,
    transaction_category_id,
    transaction_account_id,
  }) {
    return api
      .put(`/transactions-service/transactions/${transaction_id}`, {
        transaction_type,
        transaction_date,
        transaction_description,
        transaction_amount,
        transaction_category_id,
        transaction_account_id,
      })
      .then((response) => {
        return response.data;
      });
  }

  deleteTransaction(transaction_id) {
    return api
      .delete(`/transactions-service/transactions/${transaction_id}`)
      .then((response) => {
        return response.status;
      });
  }
}

export default new TransactionService();
