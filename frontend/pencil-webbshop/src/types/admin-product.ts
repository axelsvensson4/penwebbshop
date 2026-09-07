export type ProductType = 'STANDARD' | 'OUTLET'
export type Availability = 'IN_STOCK' | 'LOW_STOCK' | 'OUT_OF_STOCK'
export type ProductCondition = 'NEW' | 'USED' | 'WORN'

export interface ProductCreateInput {
  name: string
  short_description: string
  description: string
  price: number
  currency: 'SEK'
  category: string
  product_type: ProductType
  availability: Availability
  condition: ProductCondition
  active: boolean
  featured: boolean
  stock_quantity: number
}

export interface AdminProduct {
  id: number
  name: string
  slug: string
  short_description: string
  description: string
  price_ore: number
  currency: string
  category: string
  product_type: ProductType
  availability: Availability
  active: boolean
  image_url: string | null
  condition: ProductCondition
  featured: boolean
  stock_quantity: number
}
