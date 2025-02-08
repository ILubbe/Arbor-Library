import { Component } from '@angular/core';
import { SearchBarComponent } from '../../search-bar/search-bar.component';

@Component({
  selector: 'app-manage-users',
  imports: [SearchBarComponent],
  templateUrl: './manage-users.component.html',
  styleUrl: './manage-users.component.scss'
})
export class ManageUsersComponent {
    // for search
    isUserPage: boolean = true;
    isUserSearch: boolean = true;
    selectedModel: string = 'User'
    selectedField: string = '';
    fieldOptions: string[] = ['Email', 'Role', 'First Name', 'Last Name'];

  constructor() {}


}
