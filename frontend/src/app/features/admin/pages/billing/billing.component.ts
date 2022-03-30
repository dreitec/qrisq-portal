import { Component, OnInit } from '@angular/core';

interface ItemData {
  id: string;
  type: string;
  city: string;
  countriy: string;
  state: string;
  startDate: string;
  endDate: string;
  status: string;
  discount: number;
  users: number;
}

@Component({
  selector: 'qr-admin-billing',
  templateUrl: './billing.component.html',
  styleUrls: ['./billing.component.scss'],
})
export class QrAdminBillingComponent implements OnInit {
  editCache: { [key: string]: { edit: boolean; data: ItemData } } = {};
  listOfData: ItemData[] = [];
  selectedType = null;
  selectedCity = null;
  selectedCountry = null;
  selectedState = null;
  selectedStatus = null;

  constructor() {}

  ngOnInit(): void {
    const data = [];
    for (let i = 0; i < 100; i++) {
      data.unshift({
        id: `${i + 1}`,
        type: ['Country', 'State', 'City'][Math.floor(Math.random() * 3)],
        city: 'Slidell',
        countriy: 'Pinellas',
        state: 'Florida',
        startDate: '3/29/22',
        endDate: '',
        status: ['Active', 'Pending'][Math.floor(Math.random() * 2)],
        discount: Math.floor(Math.random() * 100),
        users: Math.floor(Math.random() * 1000) + 1,
      });
    }
    this.listOfData = data;
    this.updateEditCache();
  }

  startEdit(id: string): void {
    this.editCache[id].edit = true;
  }

  cancelEdit(id: string): void {
    const index = this.listOfData.findIndex((item) => item.id === id);
    this.editCache[id] = {
      data: { ...this.listOfData[index] },
      edit: false,
    };
  }

  saveEdit(id: string): void {
    const index = this.listOfData.findIndex((item) => item.id === id);
    Object.assign(this.listOfData[index], this.editCache[id].data);
    this.editCache[id].edit = false;
  }

  updateEditCache(): void {
    this.listOfData.forEach((item) => {
      this.editCache[item.id] = {
        edit: false,
        data: { ...item },
      };
    });
  }

  addRow(): void {
    // this.listOfData = [
    //   {
    //     id: `${this.listOfData.length + 1}`,
    //     type: '',
    //     city: '',
    //     countriy: '',
    //     state: '',
    //     startDate: '',
    //     endDate: '',
    //     status: '',
    //     discount: 0,
    //     users: 0,
    //   },
    //   ...this.listOfData,
    // ];
  }
}
