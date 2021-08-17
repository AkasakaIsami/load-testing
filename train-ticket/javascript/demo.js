export let options = {
    vus: 1,
    iterations: 1,
};

// export function setup() {
//     console.log("setup");
//     return { v: 1 };
//   }
  
  export default function () {
    localStorage.setItem('key', 12);
  
    console.log(localStorage.getItem('key'));
  }
  
  // export function teardown(data) {
  //     console.log("teardown");
  //   if (data.v != 1) {
  //     throw new Error('incorrect data: ' + JSON.stringify(data));
  //   }
  // }
  