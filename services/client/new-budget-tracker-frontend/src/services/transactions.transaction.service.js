import api from "./api";

class TransactionService {
  addTransaction({
    transaction_type,
    transaction_description,
    transaction_amount,
    transaction_category_id,
    transaction_account_id,
  }) {
    return api
      .post("/transactions-service/transactions", {
        transaction_type,
        transaction_description,
        transaction_amount,
        transaction_category_id,
        transaction_account_id,
      })
      .then((response) => {
        return response.data;
      });
  }

  getTransactions() {
    return api.get("/transactions-service/transactions").then((response) => {
      return response.data;
    });
  }

  editTransaction({
    transaction_id,
    transaction_type,
    transaction_description,
    transaction_amount,
    transaction_category_id,
    transaction_account_id,
  }) {
    return api
      .put(`ce/a/transactions-serviccounts/transfer/${transaction_id}`, {
        from_account_id,
        to_account_id,
        transfer_amount,
      })
      .then((response) => {
        return response.data;
      });
  }

  deleteTransaction(transaction_id) {
    return api
      .delete(`/transactions-service/accounts/transfer/${transaction_id}`)
      .then((response) => {
        return response.status;
      });
  }
}

export default new TransactionService();
