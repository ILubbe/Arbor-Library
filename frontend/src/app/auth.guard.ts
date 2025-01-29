import { CanActivateFn, Router } from '@angular/router';
import { inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { jwtDecode } from 'jwt-decode';
import { environment } from '../environments/enironment';

export const authGuard: CanActivateFn = async (route, state) => {
  const router = inject(Router);
  const http = inject(HttpClient);
  const apiEndpoint = environment.backendUrl + '/refresh';
  const accessToken = localStorage.getItem('accessToken');
  const refreshToken = localStorage.getItem('refreshToken');

  if(!accessToken) {
    return router.navigate(['/login']);
  }

  try {
    const decodedAccessToken: any = jwtDecode(accessToken);
    const expirationTime = decodedAccessToken.exp * 1000;

    // if access token and refresh tokens are in local storage and access token is expired, get a new access and refresh token.
    // if this fails (because refresh token is also expired), have to re-login.
    if(expirationTime < Date.now()) {
      if(refreshToken) {
        try {
          let headers = {
            'Authorization': `Bearer ${refreshToken}`,
            'Content-Type': 'application/json'
          }

          const response = await http
            .post<any>(apiEndpoint, {}, { headers })
            .toPromise();

          localStorage.setItem('accessToken', response.accessToken);
          localStorage.setItem('refreshToken', response.refreshToken);

          return true;

        } catch (error) {
          localStorage.removeItem('accessToken');
          localStorage.removeItem('refreshToken');
          

          return router.createUrlTree(['/login']);

        }
      } else {
        localStorage.removeItem('accessToken');

        return router.createUrlTree(['/login']);

      }
    }

    return true;

  } catch (error) {
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');

    return router.createUrlTree(['/login']);
  }
};
