import {
  SubscriptionPlansHttpGetResponseModel,
  SubscriptionPlanHttpGetResponseModel,
} from './../models/SubscriptionPlan.model';
import {
  AdminUserHttpGetResponseModel,
  AdminUsersHttpGetResponseModel,
} from './../models/AdminUser.models';
import { Observable } from 'rxjs';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { environment } from '@env';
import {
  ClientUserHttpGetResponseModel,
  ClientUsersHttpGetResponseModel,
} from '../models/ClientUser.models';

@Injectable({
  providedIn: 'root',
})
export class QrAdminService {
  constructor(private httpClient: HttpClient) {}

  /* -------------------------------------------------------------------------- */
  /*                                   admins                                   */
  /* -------------------------------------------------------------------------- */

  // /admin
  fetchAdmins(params) {
    return this.httpClient.get<AdminUsersHttpGetResponseModel>(
      environment.API_URL + '/admins',
      {
        headers: { 'Content-type': 'application/json; charset=utf-8' },
        params,
      }
    );
  }

  /* -------------------------------------------------------------------------- */
  /*                                    users                                   */
  /* -------------------------------------------------------------------------- */

  // /admin
  fetchUsers(params) {
    return this.httpClient.get<ClientUsersHttpGetResponseModel>(
      environment.API_URL + '/clients',
      {
        headers: { 'Content-type': 'application/json; charset=utf-8' },
        params,
      }
    );
  }

  fetchUser(userId) {
    return this.httpClient.get<ClientUserHttpGetResponseModel>(
      environment.API_URL + '/users/' + userId,
      {
        headers: { 'Content-type': 'application/json; charset=utf-8' },
      }
    );
  }

  searchUsers(params) {
    return this.httpClient.get(environment.API_URL + '/clients', {
      headers: { 'Content-type': 'application/json; charset=utf-8' },
      params,
    });
  }

  insertUser(params) {
    return this.httpClient.post(environment.API_URL + '/users', params, {
      headers: { 'Content-type': 'application/json; charset=utf-8' },
    });
  }

  updateUser(userId, params) {
    return this.httpClient.put(
      environment.API_URL + '/users/' + userId,
      params,
      {
        headers: { 'Content-type': 'application/json; charset=utf-8' },
      }
    );
  }

  deleteUser(userId) {
    return this.httpClient.delete(environment.API_URL + '/users/' + userId, {
      headers: { 'Content-type': 'application/json; charset=utf-8' },
    });
  }

  /* --------------------------- subscription plans --------------------------- */

  fetchSubscriptionPlans(params) {
    return this.httpClient.get<SubscriptionPlansHttpGetResponseModel>(
      environment.API_URL + '/subscription-plans',
      {
        headers: { 'Content-type': 'application/json; charset=utf-8' },
        params,
      }
    );
  }

  fetchSubscriptionPlan(subscriptionPlanId) {
    return this.httpClient.get<SubscriptionPlanHttpGetResponseModel>(
      environment.API_URL + '/subscription-plans/' + subscriptionPlanId,
      {
        headers: { 'Content-type': 'application/json; charset=utf-8' },
      }
    );
  }

  insertSubscriptionPlan(params) {
    return this.httpClient.post(
      environment.API_URL + '/subscription-plans',
      params,
      {
        headers: { 'Content-type': 'application/json; charset=utf-8' },
      }
    );
  }

  updateSubscriptionPlan(subscriptionPlanId, params) {
    return this.httpClient.put(
      environment.API_URL + '/subscription-plans/' + subscriptionPlanId,
      params,
      {
        headers: { 'Content-type': 'application/json; charset=utf-8' },
      }
    );
  }

  deleteSubscriptionPlan(subscriptionPlanId) {
    return this.httpClient.delete(
      environment.API_URL + '/subscription-plans/' + subscriptionPlanId,
      {
        headers: { 'Content-type': 'application/json; charset=utf-8' },
      }
    );
  }
}
