import { CanActivateFn } from '@angular/router';
import { inject } from '@angular/core';
import { jwtDecode } from 'jwt-decode';
import { Router } from '@angular/router';

export const librarianGuard: CanActivateFn = (route, state) => {
  const accessToken = localStorage.getItem('accessToken');
  const router = inject(Router);

  if (!accessToken) {
    router.navigate(['/login']);
    return false;
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
    router.navigate(['/login']);

    return false;

  }
};