import { CanActivateFn } from '@angular/router';
import { inject } from '@angular/core';
import { jwtDecode } from 'jwt-decode';
import { Router } from '@angular/router';
import { AuthService } from './services/auth.service';

export const librarianGuard: CanActivateFn = (route, state) => {
  const router = inject(Router);
  const authService = inject(AuthService);
  const accessToken = authService.getAccessToken();
  const refreshToken = authService.getRefreshToken();

  if (!accessToken || !refreshToken) {
    return router.createUrlTree(['/login'])
  }

  // make sure user has the librarian role in access token
  try {
    const decodedToken: any = jwtDecode(accessToken);
    if (decodedToken.role !== 'librarian') {
      router.navigate(['/home']);
      return false;
    }
    return true;
  } catch (error) {
    return authService.logout();
  }
};