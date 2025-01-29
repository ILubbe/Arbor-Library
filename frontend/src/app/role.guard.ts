import { ActivatedRouteSnapshot, RouterStateSnapshot, CanActivateFn } from '@angular/router';
import { inject } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService } from './services/auth.service';

export const roleGuard: CanActivateFn = (
  next: ActivatedRouteSnapshot,
  state: RouterStateSnapshot
) => {
  
  const router = inject(Router);
  const authService = inject(AuthService);
  const accessToken = authService.getAccessToken();
  const refreshToken = authService.getRefreshToken();

  if (!accessToken || !refreshToken) {
    return router.navigateByUrl('/login')
  }

  // make sure user has the proper role in access token
  try {
    const required_role = 'librarian';
    const userRole = authService.getUserRole();
    if (userRole !== required_role) {
      window.history.back();
      return false;
    }
    return true;
  } catch (error) {
    return authService.logout();
  }
};