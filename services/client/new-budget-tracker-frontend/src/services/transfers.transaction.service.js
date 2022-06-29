import api from "./api";

class TransactionsServiceTransfers {
  addTransfer({ from_account_id, to_account_id, transfer_amount }) {
    return api
      .post("/transactions-service/accounts/transfer", {
        from_account_id,
        to_account_id,
        transfer_amount,
      })
      .then((response) => {
        return response.data;
      });
  }

  getTransfers() {
    return api
      .get("/transactions-service/accounts/transfer")
      .then((response) => {
        return response.data;
      });
  }

  editTranfer({
    transfer_id,
    from_account_id,
    to_account_id,
    transfer_amount,
  }) {
    return api
      .put(`/transactions-service/accounts/transfer/${transfer_id}`, {
        from_account_id,
        to_account_id,
        transfer_amount,
      })
      .then((response) => {
        return response.data;
      });
  }

  deleteTransfer(transfer_id) {
    return api
      .delete(`/transactions-service/accounts/transfer/${transfer_id}`)
      .then((response) => {
        return response.status;
      });
  }
}

export default new TransactionsServiceTransfers();
